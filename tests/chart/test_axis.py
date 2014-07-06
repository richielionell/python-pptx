# encoding: utf-8

"""
Test suite for pptx.chart module
"""

from __future__ import absolute_import, print_function

import pytest

from pptx.chart.axis import _BaseAxis, TickLabels
from pptx.enum.chart import XL_TICK_MARK

from ..unitutil.cxml import element, xml
from ..unitutil.mock import class_mock, instance_mock


class Describe_BaseAxis(object):

    def it_knows_whether_it_is_visible(self, visible_get_fixture):
        axis, expected_bool_value = visible_get_fixture
        assert axis.visible is expected_bool_value

    def it_can_change_whether_it_is_visible(self, visible_set_fixture):
        axis, new_value, expected_xml = visible_set_fixture
        axis.visible = new_value
        assert axis._element.xml == expected_xml

    def it_raises_on_assign_non_bool_to_visible(self):
        axis = _BaseAxis(None)
        with pytest.raises(ValueError):
            axis.visible = 'foobar'

    def it_knows_the_scale_maximum(self, maximum_scale_get_fixture):
        axis, expected_value = maximum_scale_get_fixture
        assert axis.maximum_scale == expected_value

    def it_can_change_the_scale_maximum(self, maximum_scale_set_fixture):
        axis, new_value, expected_xml = maximum_scale_set_fixture
        axis.maximum_scale = new_value
        assert axis._element.xml == expected_xml

    def it_knows_the_scale_minimum(self, minimum_scale_get_fixture):
        axis, expected_value = minimum_scale_get_fixture
        assert axis.minimum_scale == expected_value

    def it_can_change_the_scale_minimum(self, minimum_scale_set_fixture):
        axis, new_value, expected_xml = minimum_scale_set_fixture
        axis.minimum_scale = new_value
        assert axis._element.xml == expected_xml

    def it_knows_its_major_tick_setting(self, major_tick_get_fixture):
        axis, expected_value = major_tick_get_fixture
        assert axis.major_tick_mark == expected_value

    def it_can_change_its_major_tick_mark(self, major_tick_set_fixture):
        axis, new_value, expected_xml = major_tick_set_fixture
        axis.major_tick_mark = new_value
        assert axis._element.xml == expected_xml

    def it_knows_its_minor_tick_setting(self, minor_tick_get_fixture):
        axis, expected_value = minor_tick_get_fixture
        assert axis.minor_tick_mark == expected_value

    def it_can_change_its_minor_tick_mark(self, minor_tick_set_fixture):
        axis, new_value, expected_xml = minor_tick_set_fixture
        axis.minor_tick_mark = new_value
        assert axis._element.xml == expected_xml

    def it_provides_access_to_the_tick_labels(self, tick_labels_fixture):
        axis, tick_labels_, TickLabels_, xAx = tick_labels_fixture
        tick_labels = axis.tick_labels
        TickLabels_.assert_called_once_with(xAx)
        assert tick_labels is tick_labels_

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('c:catAx',                          XL_TICK_MARK.CROSS),
        ('c:catAx/c:majorTickMark',          XL_TICK_MARK.CROSS),
        ('c:catAx/c:majorTickMark{val=out}', XL_TICK_MARK.OUTSIDE),
    ])
    def major_tick_get_fixture(self, request):
        xAx_cxml, expected_value = request.param
        axis = _BaseAxis(element(xAx_cxml))
        return axis, expected_value

    @pytest.fixture(params=[
        ('c:catAx',                         XL_TICK_MARK.INSIDE,
         'c:catAx/c:majorTickMark{val=in}'),
        ('c:catAx',                         XL_TICK_MARK.CROSS,
         'c:catAx'),
        ('c:catAx/c:majorTickMark{val=in}', XL_TICK_MARK.OUTSIDE,
         'c:catAx/c:majorTickMark{val=out}'),
        ('c:catAx/c:majorTickMark{val=in}', XL_TICK_MARK.CROSS,
         'c:catAx'),
    ])
    def major_tick_set_fixture(self, request):
        xAx_cxml, new_value, expected_xAx_cxml = request.param
        axis = _BaseAxis(element(xAx_cxml))
        expected_xml = xml(expected_xAx_cxml)
        return axis, new_value, expected_xml

    @pytest.fixture(params=[
        ('c:catAx/c:scaling/c:max{val=12.34}', 12.34),
        ('c:valAx/c:scaling/c:max{val=23.45}', 23.45),
        ('c:catAx/c:scaling',                  None),
        ('c:valAx/c:scaling',                  None),
    ])
    def maximum_scale_get_fixture(self, request):
        xAx_cxml, expected_value = request.param
        axis = _BaseAxis(element(xAx_cxml))
        return axis, expected_value

    @pytest.fixture(params=[
        ('c:catAx/c:scaling', 34.56, 'c:catAx/c:scaling/c:max{val=34.56}'),
        ('c:valAx/c:scaling', 45.67, 'c:valAx/c:scaling/c:max{val=45.67}'),
        ('c:catAx/c:scaling', None,  'c:catAx/c:scaling'),
        ('c:valAx/c:scaling/c:max{val=42.42}', 12.34,
         'c:valAx/c:scaling/c:max{val=12.34}'),
        ('c:catAx/c:scaling/c:max{val=42.42}', None,
         'c:catAx/c:scaling'),
    ])
    def maximum_scale_set_fixture(self, request):
        xAx_cxml, new_value, expected_xAx_cxml = request.param
        axis = _BaseAxis(element(xAx_cxml))
        expected_xml = xml(expected_xAx_cxml)
        return axis, new_value, expected_xml

    @pytest.fixture(params=[
        ('c:catAx/c:scaling/c:min{val=12.34}', 12.34),
        ('c:valAx/c:scaling/c:min{val=23.45}', 23.45),
        ('c:catAx/c:scaling',                  None),
        ('c:valAx/c:scaling',                  None),
    ])
    def minimum_scale_get_fixture(self, request):
        xAx_cxml, expected_value = request.param
        axis = _BaseAxis(element(xAx_cxml))
        return axis, expected_value

    @pytest.fixture(params=[
        ('c:catAx/c:scaling', 34.56, 'c:catAx/c:scaling/c:min{val=34.56}'),
        ('c:valAx/c:scaling', 45.67, 'c:valAx/c:scaling/c:min{val=45.67}'),
        ('c:catAx/c:scaling', None,  'c:catAx/c:scaling'),
        ('c:valAx/c:scaling/c:min{val=42.42}', 12.34,
         'c:valAx/c:scaling/c:min{val=12.34}'),
        ('c:catAx/c:scaling/c:min{val=42.42}', None,
         'c:catAx/c:scaling'),
    ])
    def minimum_scale_set_fixture(self, request):
        xAx_cxml, new_value, expected_xAx_cxml = request.param
        axis = _BaseAxis(element(xAx_cxml))
        expected_xml = xml(expected_xAx_cxml)
        return axis, new_value, expected_xml

    @pytest.fixture(params=[
        ('c:valAx',                            XL_TICK_MARK.CROSS),
        ('c:valAx/c:minorTickMark',            XL_TICK_MARK.CROSS),
        ('c:valAx/c:minorTickMark{val=cross}', XL_TICK_MARK.CROSS),
        ('c:valAx/c:minorTickMark{val=out}',   XL_TICK_MARK.OUTSIDE),
    ])
    def minor_tick_get_fixture(self, request):
        xAx_cxml, expected_value = request.param
        axis = _BaseAxis(element(xAx_cxml))
        return axis, expected_value

    @pytest.fixture(params=[
        ('c:valAx',                         XL_TICK_MARK.INSIDE,
         'c:valAx/c:minorTickMark{val=in}'),
        ('c:valAx',                         XL_TICK_MARK.CROSS,
         'c:valAx'),
        ('c:valAx/c:minorTickMark{val=in}', XL_TICK_MARK.OUTSIDE,
         'c:valAx/c:minorTickMark{val=out}'),
        ('c:valAx/c:minorTickMark{val=in}', XL_TICK_MARK.CROSS,
         'c:valAx'),
    ])
    def minor_tick_set_fixture(self, request):
        xAx_cxml, new_value, expected_xAx_cxml = request.param
        axis = _BaseAxis(element(xAx_cxml))
        expected_xml = xml(expected_xAx_cxml)
        return axis, new_value, expected_xml

    @pytest.fixture
    def tick_labels_fixture(self, TickLabels_, tick_labels_):
        xAx = element('c:valAx')
        axis = _BaseAxis(xAx)
        return axis, tick_labels_, TickLabels_, xAx

    @pytest.fixture(params=[
        ('c:catAx',                     False),
        ('c:catAx/c:delete',            False),
        ('c:catAx/c:delete{val=0}',     True),
        ('c:catAx/c:delete{val=1}',     False),
        ('c:catAx/c:delete{val=false}', True),
        ('c:valAx',                     False),
        ('c:valAx/c:delete',            False),
        ('c:valAx/c:delete{val=0}',     True),
        ('c:valAx/c:delete{val=1}',     False),
        ('c:valAx/c:delete{val=false}', True),
    ])
    def visible_get_fixture(self, request):
        xAx_cxml, expected_bool_value = request.param
        axis = _BaseAxis(element(xAx_cxml))
        return axis, expected_bool_value

    @pytest.fixture(params=[
        ('c:catAx',                 True,  'c:catAx/c:delete{val=0}'),
        ('c:catAx',                 False, 'c:catAx/c:delete'),
        ('c:valAx/c:delete',        True,  'c:valAx/c:delete{val=0}'),
        ('c:catAx/c:delete',        False, 'c:catAx/c:delete'),
        ('c:catAx/c:delete{val=1}', True,  'c:catAx/c:delete{val=0}'),
        ('c:valAx/c:delete{val=1}', False, 'c:valAx/c:delete'),
        ('c:valAx/c:delete{val=0}', True,  'c:valAx/c:delete{val=0}'),
        ('c:catAx/c:delete{val=0}', False, 'c:catAx/c:delete'),
    ])
    def visible_set_fixture(self, request):
        xAx_cxml, new_value, expected_xAx_cxml = request.param
        axis = _BaseAxis(element(xAx_cxml))
        expected_xml = xml(expected_xAx_cxml)
        return axis, new_value, expected_xml

    # fixture components ---------------------------------------------

    @pytest.fixture
    def TickLabels_(self, request, tick_labels_):
        return class_mock(
            request, 'pptx.chart.axis.TickLabels',
            return_value=tick_labels_
        )

    @pytest.fixture
    def tick_labels_(self, request):
        return instance_mock(request, TickLabels)


class DescribeTickLabels(object):

    def it_knows_its_number_format(self, number_format_get_fixture):
        tick_labels, expected_value = number_format_get_fixture
        assert tick_labels.number_format == expected_value

    def it_can_change_its_number_format(self, number_format_set_fixture):
        tick_labels, new_value, expected_xml = number_format_set_fixture
        tick_labels.number_format = new_value
        assert tick_labels._element.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('c:catAx',                              'General'),
        ('c:valAx/c:numFmt{formatCode=General}', 'General'),
    ])
    def number_format_get_fixture(self, request):
        xAx_cxml, expected_value = request.param
        tick_labels = TickLabels(element(xAx_cxml))
        return tick_labels, expected_value

    @pytest.fixture(params=[
        ('c:catAx', 'General', 'c:catAx/c:numFmt{formatCode=General}'),
        ('c:valAx/c:numFmt{formatCode=General}', '00.00',
         'c:valAx/c:numFmt{formatCode=00.00}'),
    ])
    def number_format_set_fixture(self, request):
        xAx_cxml, new_value, expected_xAx_cxml = request.param
        tick_labels = TickLabels(element(xAx_cxml))
        expected_xml = xml(expected_xAx_cxml)
        return tick_labels, new_value, expected_xml