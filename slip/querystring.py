def select_normal_slipinput(start_date=None, end_date=None, sq_acttax2=None):
    """
    일반전표입력 조회 쿼리
    :param date: 해당날짜(일을 API에서 입력받았을 경우)
    :param start_date: 시작날짜(일을 입력받지 않았을 경우, 해당 년도, 월의 1일.)
    :param end_date: 종료날짜(일을 입력받지 않았을 경우, 해댱 년도, 월의 마지막 날.)
    :return: SELECT query
    """
    query = """
            SELECT 	DISTINCT a.da_date, a.sq_acttax2,
                SUBSTR(a.da_date, 1, 4) AS year,
                SUBSTR(a.da_date, 5, 2) AS month,
                SUBSTR(a.da_date, 7, 2) AS day,
                a.cd_trade, a.nm_trade, a.cd_remark, a.nm_remark,
                CASE a.ty_gubn
                    WHEN 1 THEN '출금'
                    WHEN 2 THEN '입금'
                    WHEN 3 THEN '차변'
                    WHEN 4 THEN '대변'
                    WHEN 5 THEN '결차'
                    WHEN 6 THEN '결대'
                END AS nm_gubn, a.ty_gubn,
                a.cd_acctit, a.key_acctit, b.nm_acctit,
                CASE WHEN a.ty_gubn IN (1,2,3,5) THEN a.mn_bungae ELSE 0
                      END AS mn_bungae1,
                CASE WHEN a.ty_gubn IN (1,2,4,6) THEN a.mn_bungae ELSE 0
                      END AS mn_bungae2,
                a.no_acct, a.cd_deptemp, a.cd_field ,a.cd_pjt,
                c.nm_deptemp as nm_dept ,d.nm_field ,e.nm_project,
                a.cd_finance ,f.nm_fitem as nm_finance ,a.yn_card,
                coalesce(g.nm_cardgb,1) as nm_cardgb,
                a.cd_jepum ,h.nm_goods as nm_jepum ,a.cd_bjoh ,
                i.nm_bjoh ,a.nm_linecolor ,a.yn_use, a.ty_copy ,
                a.no_exter2 ,a.ty_bungae ,a.nm_memot ,a.nm_memo ,
                a.sq_bungae, a.no_car ,a.no_carbody ,a.dt_insert,
                a.sq_sbguid
            FROM fta_acttax2 AS a
            LEFT OUTER JOIN ftb_acctcd AS b ON a.key_acctit=b.key_acctit
            LEFT OUTER JOIN fta_deptemp AS c ON a.cd_deptemp=c.cd_deptemp
            LEFT OUTER JOIN ftb_field AS d ON a.cd_field=d.cd_field
            LEFT OUTER JOIN ftb_pjt AS e ON a.cd_pjt=e.cd_project
            LEFT OUTER JOIN fta_fitem AS f ON a.cd_finance=f.cd_fitem
            LEFT OUTER JOIN fta_supply AS g ON a.sq_acttax2=g.sq_acttax2
            LEFT OUTER JOIN fth_goods AS h ON a.cd_jepum=h.cd_goods
            LEFT OUTER JOIN ftb_bitem AS i ON a.cd_bjoh=i.cd_bjoh
            """
    query += """WHERE (a.no_acct <= 50000) """
    if sq_acttax2:
        query += "and (a.sq_acttax2 = %s)" %(sq_acttax2)

    if start_date and end_date:
        query += """AND  (a.da_date >= '%s' AND a.da_date <= '%s') """ % (start_date, end_date)

    query += """ORDER BY a.da_date, a.no_acct, a.sq_bungae, a.sq_acttax2"""

    return query

'''
주석
'''


def select_cash_balance(start_date=None, end_date=None):
    query = """
        select
                (
                    (select coalesce(sum(mn_forw),0) as cashsum from fta_bsforw where cd_acctit='10100' and ty_year=0)
                      +
                    (select
        			    coalesce(sum(
    				                case
    				                    when ty_gubn=1 then mn_bungae*-1
    					                when ty_gubn=2 then mn_bungae*1
    					                when(ty_gubn=3 or ty_gubn=5) and cd_acctit='10100' then mn_bungae*1
    					                when(ty_gubn=4 or ty_gubn=6) and cd_acctit='10100' then mn_bungae*-1
    					                else 0
    				                end), 0) as cashsum
    		         from fta_acttax2
    		         where da_date between '%s' and '%s')
                ) as sum
        """ % (start_date, end_date)

    return query