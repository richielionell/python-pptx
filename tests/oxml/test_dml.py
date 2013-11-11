# encoding: utf-8

"""
Test suite for pptx.oxml.dml module.
"""

from __future__ import absolute_import, print_function

import pytest

from pptx.oxml.dml import (
    CT_Percentage, CT_SchemeColor, CT_SRgbColor, CT_SolidColorFillProperties
)
from pptx.oxml.ns import qn

from ..oxml.unitdata.dml import (
    a_lumMod, a_lumOff, a_prstClr, a_schemeClr, a_solidFill, an_srgbClr
)
from ..unitutil import actual_xml


class DescribeCT_Percentage(object):

    def it_is_used_by_the_parser_for_a_lumOff_element(self, lumOff):
        assert isinstance(lumOff, CT_Percentage)

    def it_is_used_by_the_parser_for_a_lumMod_element(self, lumMod):
        assert isinstance(lumMod, CT_Percentage)

    def it_knows_the_percentage_str_value(self, ct_percentage):
        assert ct_percentage.val == '99999'

    # fixtures ---------------------------------------------

    @pytest.fixture
    def ct_percentage(self):
        return a_lumMod().with_nsdecls().with_val('99999').element

    @pytest.fixture
    def lumMod(self):
        return a_lumMod().with_nsdecls().with_val('33333').element

    @pytest.fixture
    def lumOff(self):
        return a_lumOff().with_nsdecls().with_val('66666').element


class DescribeCT_SchemeColor(object):

    def it_is_used_by_the_parser_for_a_schemeClr_element(self, schemeClr):
        assert isinstance(schemeClr, CT_SchemeColor)

    def it_knows_the_theme_color_str_value(self, schemeClr):
        assert schemeClr.val == 'bg1'

    def it_can_get_the_lumMod_child_element_if_there_is_one(
            self, schemeClr, schemeClr_with_lumMod, lumMod):
        assert schemeClr.lumMod is None
        assert schemeClr_with_lumMod.lumMod is lumMod

    def it_can_get_the_lumOff_child_element_if_there_is_one(
            self, schemeClr, schemeClr_with_lumOff, lumOff):
        assert schemeClr.lumOff is None
        assert schemeClr_with_lumOff.lumOff is lumOff

    # fixtures ---------------------------------------------

    @pytest.fixture
    def schemeClr(self):
        return a_schemeClr().with_nsdecls().with_val('bg1').element

    @pytest.fixture
    def schemeClr_with_lumMod(self, lumMod):
        schemeClr = a_schemeClr().with_nsdecls().element
        schemeClr.append(lumMod)
        return schemeClr

    @pytest.fixture
    def schemeClr_with_lumOff(self, lumOff):
        schemeClr = a_schemeClr().with_nsdecls().element
        schemeClr.append(lumOff)
        return schemeClr

    @pytest.fixture
    def lumMod(self):
        return a_lumMod().with_nsdecls().element

    @pytest.fixture
    def lumOff(self):
        return a_lumOff().with_nsdecls().element


class DescribeCT_SRgbColor(object):

    def it_is_used_by_the_parser_for_an_srgbClr_element(self, srgbClr):
        assert isinstance(srgbClr, CT_SRgbColor)

    def it_knows_the_rgb_str_value(self, srgbClr):
        assert srgbClr.val == '123456'

    def it_can_get_the_lumMod_child_element_if_there_is_one(
            self, srgbClr, srgbClr_with_lumMod, lumMod):
        assert srgbClr.lumMod is None
        assert srgbClr_with_lumMod.lumMod is lumMod

    def it_can_get_the_lumOff_child_element_if_there_is_one(
            self, srgbClr, srgbClr_with_lumOff, lumOff):
        assert srgbClr.lumOff is None
        assert srgbClr_with_lumOff.lumOff is lumOff

    def it_can_set_the_rgb_str_value(self, srgbClr, srgbClr_xml):
        srgbClr.val = '987654'
        assert actual_xml(srgbClr) == srgbClr_xml

    # fixtures ---------------------------------------------

    @pytest.fixture
    def srgbClr(self):
        return an_srgbClr().with_nsdecls().with_val('123456').element

    @pytest.fixture
    def srgbClr_xml(self):
        return an_srgbClr().with_nsdecls().with_val('987654').xml()

    @pytest.fixture
    def srgbClr_with_lumMod(self, lumMod):
        srgbClr = an_srgbClr().with_nsdecls().element
        srgbClr.append(lumMod)
        return srgbClr

    @pytest.fixture
    def srgbClr_with_lumOff(self, lumOff):
        srgbClr = an_srgbClr().with_nsdecls().element
        srgbClr.append(lumOff)
        return srgbClr

    @pytest.fixture
    def lumMod(self):
        return a_lumMod().with_nsdecls().element

    @pytest.fixture
    def lumOff(self):
        return a_lumOff().with_nsdecls().element


class DescribeCT_SolidColorFillProperties(object):

    def it_is_used_by_the_parser_for_a_solidFill_element(self, solidFill):
        assert isinstance(solidFill, CT_SolidColorFillProperties)

    def it_can_get_the_schemeClr_child_element_or_None_if_there_isnt_one(
            self, solidFill, solidFill_with_schemeClr, schemeClr):
        assert solidFill.schemeClr is None
        assert solidFill_with_schemeClr.schemeClr is schemeClr

    def it_can_get_the_srgbClr_child_element_or_None_if_there_isnt_one(
            self, solidFill, solidFill_with_srgbClr, srgbClr):
        assert solidFill.srgbClr is None
        assert solidFill_with_srgbClr.srgbClr is srgbClr

    def it_gets_the_srgbClr_child_element_if_there_is_one(
            self, solidFill_with_srgbClr, srgbClr):
        _srgbClr = solidFill_with_srgbClr.get_or_change_to_srgbClr()
        assert _srgbClr is srgbClr

    def it_adds_an_srgbClr_child_element_if_there_isnt_one(
            self, solidFill, solidFill_with_srgbClr_xml):
        srgbClr = solidFill.get_or_change_to_srgbClr()
        assert actual_xml(solidFill) == solidFill_with_srgbClr_xml
        assert solidFill.find(qn('a:srgbClr')) == srgbClr

    def it_changes_the_color_choice_to_srgbClr_if_a_different_one_is_there(
            self, solidFill_with_schemeClr, solidFill_with_prstClr,
            solidFill_with_srgbClr_xml):
        for elm in (solidFill_with_schemeClr, solidFill_with_prstClr):
            elm.get_or_change_to_srgbClr()
            assert actual_xml(elm) == solidFill_with_srgbClr_xml

    # fixtures ---------------------------------------------

    @pytest.fixture
    def solidFill(self):
        return a_solidFill().with_nsdecls().element

    @pytest.fixture
    def solidFill_with_prstClr(self):
        prstClr_bldr = a_prstClr()
        solidFill_bldr = a_solidFill().with_nsdecls().with_child(prstClr_bldr)
        return solidFill_bldr.element

    @pytest.fixture
    def solidFill_with_schemeClr(self, schemeClr):
        solidFill = a_solidFill().with_nsdecls().element
        solidFill.append(schemeClr)
        return solidFill

    @pytest.fixture
    def solidFill_with_srgbClr(self, srgbClr):
        solidFill = a_solidFill().with_nsdecls().element
        solidFill.append(srgbClr)
        return solidFill

    @pytest.fixture
    def solidFill_with_srgbClr_xml(self):
        srgbClr_bldr = an_srgbClr()
        return a_solidFill().with_nsdecls().with_child(srgbClr_bldr).xml()

    @pytest.fixture
    def schemeClr(self):
        return a_schemeClr().with_nsdecls().element

    @pytest.fixture
    def srgbClr(self):
        return an_srgbClr().with_nsdecls().element
