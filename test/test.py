#!/bin/env python

""" Unit test output of color_config command """

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(__file__ + '/../../')) # ../test/test.py -> ../
from source import color_config # pylint: disable=wrong-import-position

# pylint: disable=too-many-public-methods
class TestColorConfig(unittest.TestCase):
	""" Test color_config command """

	@classmethod
	def setUpClass(cls):
		""" Run before all the tests """
		cls.test_paths = []
		dirname = os.path.dirname(os.path.realpath(__file__))
		for i in range(0, 30):
			cls.test_paths.append(os.path.join(dirname, 'test' + str(i) + '.yaml'))

	@classmethod
	def tearDownClass(cls):
		""" Cleanup all output files after all the tests except test1.vim """
		os.remove('test1.vim')

	def setUp(self):
		""" Run before every test """
		pass

	def tearDown(self):
		""" Run after every test """
		pass

	def test_cmd(self):
		""" Test command exit status """
		self.assertEqual(os.system('../source/color_config.py ' + self.test_paths[1]), 0)

	def test_rgb2hex(self):
		""" Test hex2rgb() """
		self.assertEqual(color_config.hex2rgb('#1234ab'), 'rgb(18, 52, 171)')
		self.assertEqual(color_config.hex2rgb('#000000'), 'rgb(0, 0, 0)')
		self.assertEqual(color_config.hex2rgb('#ffffff'), 'rgb(255, 255, 255)')

	def test_hex2rgb(self):
		""" Test rgb2hex() """
		self.assertEqual(color_config.rgb2hex('rgb(1, 100, 200)'), '#0164c8')
		self.assertEqual(color_config.rgb2hex('rgb(34,   99,  0)'), '#226300')
		self.assertEqual(color_config.rgb2hex('rgb(255,6,43)'), '#ff062b')

	def test_author_is_empty(self):
		""" Test fail when empty author field dont raise exception NameError """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[2])
		with self.assertRaises(NameError):
			color_config.get_author()

		color_config.color_dict = color_config.parse_yaml(self.test_paths[3])
		with self.assertRaises(NameError):
			color_config.get_author()

	def test_default_description(self):
		""" Test default description is which should be '<name> colorscheme' """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[4])
		self.assertEqual(color_config.get_description(), 'test4 colorscheme')

	def test_background_option(self):
		""" Test: default background should be 'dark', value should be 'dark' or 'light' only """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[5])
		self.assertEqual(color_config.get_background(), 'dark')

		color_config.color_dict = color_config.parse_yaml(self.test_paths[6])
		self.assertEqual(color_config.get_background(), 'dark')

		color_config.color_dict = color_config.parse_yaml(self.test_paths[7])
		with self.assertRaises(NameError):
			color_config.get_background()

	def test_name_is_empty(self):
		""" Test fail when empty name field dont raise exception NameError """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[8])
		with self.assertRaises(NameError):
			color_config.get_name()

		color_config.color_dict = color_config.parse_yaml(self.test_paths[9])
		with self.assertRaises(NameError):
			color_config.get_name()

	def test_color_name_is_in_palette(self):
		""" Test if color name is in color palette """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[10])
		color_config.set_up(color_config.color_dict)

		with self.assertRaises(NameError):
			color_config.get_hi_group_value('Normal')
		with self.assertRaises(NameError):
			color_config.get_hi_group_value('Comment')

	def test_attr_val_is_valid_name(self):
		""" Test if attribute value is a valid name """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[11])
		color_config.set_up(color_config.color_dict)

		with self.assertRaises(NameError):
			color_config.get_hi_group_value('Comment')

	def test_color_group_has_minimum_value(self):
		"""
		Test if color group has at least 3 value (bg color, fg color and attribute)
		'_' is also a value indicate NONE
		"""
		color_config.color_dict = color_config.parse_yaml(self.test_paths[12])
		color_config.set_up(color_config.color_dict)

		with self.assertRaises(ValueError):
			color_config.get_hi_group_value('Normal')
		with self.assertRaises(ValueError):
			color_config.get_hi_group_value('Comment')

	def test_transparent_option(self):
		""" Test if transparent is true, ctermbg in transp group is NONE  """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[13])
		color_config.set_up(color_config.color_dict)

		transp_group = ['Normal', 'LineNr', 'Folded', 'SignColumn']
		for group in transp_group:
			if group in color_config.color_dict['group']:
				err_msg = ('trasparent is set. {} group ctermbg should be NONE, '
						'found {} instead ').format(group, color_config.get_hi_group_value(group)[1])
				self.assertEqual(color_config.get_hi_group_value(group)[1], 'NONE', err_msg)

	def test_colorname_transform(self):
		""" Test transform color name to lowercase """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[14])
		color_config.set_up(color_config.color_dict)

		self.assertTrue(color_config.get_group_dict()['Normal'].islower())
		self.assertTrue(color_config.get_group_dict()['Comment'].islower())

		self.assertIn('dark', color_config.get_colors())
		self.assertIn('gray', color_config.get_colors())
		self.assertIn('snow', color_config.get_colors())

	def test_multiple_attribute(self):
		""" Test multiple attribute getters """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[15])

		color_config.set_up(color_config.color_dict)

		self.assertEqual(color_config.get_hi_group_value('Normal')[4], 'reverse')
		self.assertEqual(color_config.get_hi_group_value('Comment')[4], 'reverse,bold,underline')
		self.assertEqual(color_config.get_hi_group_value('Identify')[4], 'reverse,bold')
		with self.assertRaises(NameError):
			color_config.get_hi_group_value('Function')
		self.assertEqual(color_config.get_hi_group_value('PreProc')[4], 'NONE')

	def test_empty_group(self):
		""" empty group should throw error """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[16])

		with self.assertRaises(KeyError):
			color_config.set_up(color_config.color_dict)

	def test_empty_palette(self):
		""" empty palette should throw error """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[17])

		with self.assertRaises(KeyError):
			color_config.set_up(color_config.color_dict)

	def test_transparent_group_option(self):
		""" transparent group option should override default transparent group """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[18])

		self.assertEqual(color_config.get_transparent_group(), ['Normal', 'Statusline'])

	def test_no_transparent_group_option(self):
		""" omit transparent group option should return default transparent group """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[19])

		self.assertEqual(color_config.get_transparent_group(), color_config.default_transparent_group)

	def test_valid_assignment_notation_for_linking_group(self):
		""" link assignment notation should be '->' """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[20])

		with self.assertRaises(ValueError):
			color_config.parse_link(color_config.get_links(0))
		self.assertEqual(color_config.parse_link(color_config.get_links(1)), ['htmlItalic', 'Normal'])

	def test_number_of_operands_of_link_statement(self):
		""" link assignment syntax should be 'group1 -> group2' """
		color_config.color_dict = color_config.parse_yaml(self.test_paths[21])

		with self.assertRaises(ValueError):
			color_config.parse_link(color_config.parse_link(color_config.get_links(0)))
		with self.assertRaises(ValueError):
			color_config.parse_link(color_config.parse_link(color_config.get_links(1)))

if __name__ == '__main__':
	unittest.main()

# vim: nofoldenable
