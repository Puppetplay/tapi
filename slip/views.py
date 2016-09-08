from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.db import connection

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from tapi.jsonutil import name_to_json, json_result

import psycopg2

from slip.querystring import select_normal_slipinput, select_cash_balance


@api_view(['POST'])
def select_data1(request):
    from_date = request.data["date_from"]
    to_date = request.data["date_to"]
    query = select_normal_slipinput(from_date, to_date)
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = name_to_json(cursor)
        data = {
            'data': rows,
            'length': len(rows),
        }
    except psycopg2.Error:
        print("error")
    result = Response(json_result(stat=status.HTTP_200_OK, data=data))
    return result


@api_view(['GET'])
def select_data(request, from_date, to_date):
    query = select_normal_slipinput(start_date = from_date, end_date=to_date)
    try:
        state = status.HTTP_200_OK
        cursor = connection.cursor()
        cursor.execute(query)
        rows = name_to_json(cursor)
        data = {
            'data': rows,
            'length': len(rows),
        }
    except psycopg2.Error:
        state = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {}
    result = Response(json_result(stat=state, data=data))
    return result



@api_view(['GET'])
def cash_balnce(request, from_date, to_date):
    query = select_cash_balance(from_date, to_date)
    try:
        state = status.HTTP_200_OK
        cursor = connection.cursor()
        cursor.execute(query)
        rows = name_to_json(cursor)
        data = {
            'data': rows,
            'length': len(rows),
        }
    except psycopg2.Error:
        state = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {}
    result = Response(json_result(stat=state, data=data))
    return result


@api_view(['GET'])
def get_data(request):
    query = 'select * from ftb_trade '
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = name_to_json(cursor)
        data = {
            'data': rows,
            'length': len(rows),
        }
    except psycopg2.Error:
        print("error")
    result = Response(json_result(stat=status.HTTP_200_OK, data=data))
    return result


@api_view(['PUT'])
def update_data(request):
    sq_acttax2 = request.data["sq_acttax2"]
    update = request.data["update"]
    #    column = request.data["column"]
    #    value = request.data["value"]
    #    another = request.data["another"]
    query = 'update fta_acttax2 '
    subqry = ''
    for cont in update:
        if subqry:
            subqry += ' ,'
        else:
            subqry = ' set'
        subqry += ' %s = \'%s\'' % (cont["column"], cont["value"])

    query += subqry
    #   query += ' set %s = %s %s' % (column, value, another)

    query += ' where sq_acttax2 = %s' % (sq_acttax2)

    #column = request.data["column"]
    #value = request.data["value"]
    #another = request.data["another"]
    #query = 'update fta_acttax2 '
    #query += ' set %s = %s %s' % (column, value, another)
    #query += ' where sq_acttax2 = %s' %(sq_acttax2)

    try:
        state = status.HTTP_200_OK
        cursor = connection.cursor()
        cursor.execute(query)
    except psycopg2.Error:
        state = status.HTTP_500_INTERNAL_SERVER_ERROR

    result = Response(json_result(stat=status.HTTP_200_OK))
    return result


@api_view(['DELETE'])
def delete_data(request):
    sq_acttax2 = request.data["sq_acttax2"]

    #if sq_acttax2:
    #    sq_acttax2 = eval(sq_acttax2)
    if(type(sq_acttax2)) is list :
        sq_acttax2 = tuple(sq_acttax2)

    query = 'delete from fta_acttax2 '
    if len(sq_acttax2) is 1 :
        query += ' where sq_acttax2 = %s' % (sq_acttax2[0])
    else:
        query += ' where sq_acttax2 in %s' % (str(sq_acttax2))

#    query = 'delete from fta_acttax2 '
#   query += ' where sq_acttax2 = %s' % (sq_acttax2)

    try:
        state = status.HTTP_200_OK
        cursor = connection.cursor()
        cursor.execute(query)
    except psycopg2.Error:
        state = status.HTTP_500_INTERNAL_SERVER_ERROR

    result = Response(json_result(stat=state))
    return result

@api_view(['POST'])
def insert_data(request):
    try:
    #NOT NULL항목
        da_date = request.data["da_date"]
        ty_gubn = request.data["ty_gubn"]
        key_acctit = request.data["key_acctit"]
        cd_acctit = request.data["cd_acctit"]
        mn_bungae = request.data["mn_bungae"]
    #NOT NULL항목 종료
        cd_trade = request.data["cd_trade"]
        nm_trade = request.data["nm_trade"]
        cd_remark = request.data["cd_remark"]
        nm_remark = request.data["nm_remark"]

        query = 'insert into fta_acttax2 (da_date, ty_gubn, key_acctit, cd_acctit, mn_bungae, cd_trade, nm_trade, cd_remark, nm_remark, id_insert, dt_insert)'
        query += ' values(\'%s\', \'%s\', \'%s\', \'%s\', %s, \'%s\', \'%s\', \'%s\', \'%s\', \'admin\', now())' % (da_date, ty_gubn,  key_acctit, cd_acctit, mn_bungae, cd_trade, nm_trade, cd_remark, nm_remark)
        query += ' returning sq_acttax2, no_acct, sq_bungae;'

        try:
            state = status.HTTP_200_OK
            cursor = connection.cursor()
            cursor.execute(query)
            rows = name_to_json(cursor)
            data = {
                'data': rows,
                'length': len(rows),
            }
        except psycopg2.Error:
            state = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {}

    except :
        state = status.HTTP_417_EXPECTATION_FAILED
        data = {}


    result = Response(json_result(stat=state, data=data))
    return result


@api_view(['PUT', 'DELETE'])
def detail_data1(request, question_id):
    sq_acttax2 = question_id
    if request.method == "PUT":
        query = 'update fta_acttax2 '
        subqry = ''

        for key in request.data.keys():
            if subqry:
                subqry += ' ,'
            else:
                subqry = ' set'
            subqry += ' %s = \'%s\'' % (key, request.data[key])

        query += subqry

        query += ' where sq_acttax2 = %s;' % (sq_acttax2)

        query += select_normal_slipinput(sq_acttax2 = sq_acttax2)
        try:
            state = status.HTTP_200_OK
            cursor = connection.cursor()
            cursor.execute(query)
            rows = name_to_json(cursor)
            data = {
                'data': rows,
                'length': len(rows),
            }
        except psycopg2.Error:
            state = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {}

        result = Response(json_result(stat=state, data=data))

    elif  request.method == "DELETE":
        query = 'delete from fta_acttax2 '
        query += ' where sq_acttax2 = %s' % (sq_acttax2)

        try:
            state = status.HTTP_200_OK
            cursor = connection.cursor()
            cursor.execute(query)
        except psycopg2.Error:
            state = status.HTTP_500_INTERNAL_SERVER_ERROR

        result = Response(json_result(stat=state))

    return result


@api_view(['GET','POST','PUT','DELETE'])
def basic_view(request, from_date="", to_date=""):
    if request.method == "GET":
        return select_data(request, from_date=from_date, to_date=to_date)
    elif request.method == "POST":
        return  insert_data(request)
    elif request.method == "PUT":
        return  update_data(request)
    else :
        return delete_data(request)


