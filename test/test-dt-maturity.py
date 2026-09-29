#!/usr/bin/env python3
#
# Testcases for the 'maturity: experimental' meta-schema
# (dtschema/meta-schemas/experimental.yaml).
#
# SPDX-License-Identifier: BSD-2-Clause
#
# Testcases are executed by running 'make test' from the top level
# directory of this repo, alongside test-dt-validate.py.

import copy
import os
import unittest

import jsonschema

import dtschema

basedir = os.path.dirname(__file__)


class TestExperimentalMetaSchema(unittest.TestCase):
    def setUp(self):
        self.schema = dtschema.DTSchema(
            os.path.join(basedir, 'schemas/experimental-widget.yaml'))

    def test_experimental_schema_valid(self):
        '''A well-formed experimental binding validates against
        experimental.yaml despite having no additionalProperties/
        unevaluatedProperties.'''
        self.schema.is_valid(strict=True)

    def test_maturity_required(self):
        '''maturity can't be dropped while $schema still points at
        experimental.yaml#.'''
        schema_tmp = copy.deepcopy(self.schema)
        del schema_tmp['maturity']
        self.assertRaises(
            jsonschema.SchemaError, schema_tmp.is_valid, strict=True)

    def test_maturity_value_is_checked(self):
        schema_tmp = copy.deepcopy(self.schema)
        schema_tmp['maturity'] = 'not-a-real-maturity-level'
        self.assertRaises(
            jsonschema.SchemaError, schema_tmp.is_valid, strict=True)

    def test_unknown_property_not_allowed(self):
        '''maturity has no companion property: an unrecognised extra
        key is rejected by propertyNames, same as any other unknown
        key.'''
        schema_tmp = copy.deepcopy(self.schema)
        schema_tmp['vendor,unknown-property'] = 'v7.10'
        self.assertRaises(
            jsonschema.SchemaError, schema_tmp.is_valid, strict=True)

    def test_maturity_properties_rejected_by_core_schema(self):
        '''A binding using core.yaml# (the normal, stable metaschema)
        must not be able to sneak the maturity property in -- it is
        only meaningful, and only allowed, under experimental.yaml#.
        '''
        schema_tmp = copy.deepcopy(self.schema)
        schema_tmp['$schema'] = 'http://devicetree.org/meta-schemas/core.yaml#'
        schema_tmp['additionalProperties'] = False
        self.assertRaises(
            jsonschema.SchemaError, schema_tmp.is_valid, strict=True)


if __name__ == '__main__':
    unittest.main()
