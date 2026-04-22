# -*- coding: utf-8 -*-
import json

from google.auth.transport import requests
from odoo import http
from odoo.http import request, Response
import requests

class MyApiClass(http.Controller):


	headers = {
		'Content-Type': 'application/json',
	}

	data = '{"params": {"username":"username","password":"pwd"}}'

	requests.post('https://...', headers=headers, data=data)

	@http.route("https://...", auth='none', type='http', method=['POST'], cors='*')
	def get_api_method(self, *kw):
		partners = request['res.partners'].sudo().search_read([])

		headers = {'Content-Type': 'application/json'}
		body = { 'params': { 'username': "username", 'password': "pwd" } }

		return Response(json.dumps(body), headers=headers)


	@http.route("http://...", auth='api_key', type='http', method=['GET'], csrf=False, cors='*')
	def post_api_method(self, email, *kw):
		partners = request['res.partners'].sudo().search_read([('email','=',email)])

		headers = {'Content-Type': 'application/json'}
		body = { 'params': { 'token': "t" } }

		return Response(json.dumps(body), headers=headers)