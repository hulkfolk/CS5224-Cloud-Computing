import os

import mysql.connector


def get_logger():
    import logging

    logger = logging.getLogger(__name__)
    hdlr = logging.FileHandler(os.path.join(os.path.dirname(__file__), '..', 'housenanny.log'))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    return logger


logger = get_logger()


def create_connection():
    # return mysql.connector.connect(host='housenanny.cuxxg96vzai9.us-east-1.rds.amazonaws.com',
    #                                database='HouseNanny',
    #                                user='HouseNanny',
    #                                password='HouseNanny')
    return mysql.connector.connect(host='localhost',
                                   database='housenannyDB',
                                   user='root',
                                   password='cloud12345')


def get_schools(args: dict):
    connection = create_connection()

    if connection.is_connected():
        if not args:
            query = f"select school_name as schoolName, address, postal_code as postalCode, " \
                    f"philosophy_culture_ethos as philosophyCultureEthos, dgp_code as dgpCode, zone_code as zoneCode, " \
                    f"cluster_code as clusterCode, type_code as typeCode, nature_code as natureCode, " \
                    f"mothertongue1_code as mothertongue1Code, mothertongue2_code as mothertongue2Code, " \
                    f"mothertongue3_code as mothertongue3Code, special_sdp_offered as specialSdpOffered, latitude, " \
                    f"longitude, mrt_desc as mrtDesc, bus_desc as busDesc, ranking " \
                    f"from primaryschool order by ranking DESC"
        else:
            name = "'%%'" if not args.get('name', None) else f"'%{args.get('name')}%'"

            if not args.get('mrt', None):
                mrt = ''
            else:
                mrt = 'AND ('
                first_arg = True
                mrt_args = args.get('mrt').split('$')
                for arg in mrt_args:
                    if first_arg:
                        mrt += f"mrt_desc like '%{arg}%'"
                        first_arg = False
                    else:
                        mrt += f" OR mrt_desc like '%{arg}%'"
                mrt += ')'

            if not args.get('area', None):
                area = ''
            else:
                area = 'AND ('
                first_arg = True
                area_args = args.get('area').split('$')
                for arg in area_args:
                    if first_arg:
                        area += f"dgp_code like '%{arg}%'"
                        first_arg = False
                    else:
                        area += f" OR dgp_code like '%{arg}%'"
                area += ')'

            if not args.get('lang', None):
                lang = ''
            else:
                lang = 'AND ('
                first_arg = True
                lang_args = args.get('lang').split('$')
                for arg in lang_args:
                    if first_arg:
                        lang += f"(mothertongue1_code='{arg}' OR mothertongue2_code='{arg}' OR mothertongue3_code='{arg}')"
                        first_arg = False
                    else:
                        lang += f" AND (mothertongue1_code='{arg}' OR mothertongue2_code='{arg}' OR mothertongue3_code='{arg}')"
                lang += ')'

            if not args.get('offering', None):
                offering = ''
            else:
                offering = 'AND ('
                first_arg = True
                offering_args = args.get('offering').split('$')
                for arg in offering_args:
                    if first_arg:
                        offering += f"special_sdp_offered like '%{arg}%'"
                        first_arg = False
                    else:
                        offering += f" OR special_sdp_offered like '%{arg}%'"
                offering += ')'

            query = f"select school_name as schoolName, address, postal_code as postalCode, " \
                    f"philosophy_culture_ethos as philosophyCultureEthos, dgp_code as dgpCode, zone_code as zoneCode, " \
                    f"cluster_code as clusterCode, type_code as typeCode, nature_code as natureCode, " \
                    f"mothertongue1_code as mothertongue1Code, mothertongue2_code as mothertongue2Code, " \
                    f"mothertongue3_code as mothertongue3Code, special_sdp_offered as specialSdpOffered, latitude, " \
                    f"longitude, mrt_desc as mrtDesc, bus_desc as busDesc, ranking " \
                    f"from primaryschool " \
                    f"where school_name like {name} {mrt} {area} {lang} {offering}"
        # print("query: ", query)
        logger.info(f"get school query: {query}")
        cursor = connection.cursor()
        cursor.execute(query)
        column_names = [col[0] for col in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        # print("query result: ", data)
        connection.close()
        return data
    else:
        return "DB is not connected"


def get_properties_by_school(args: dict):
    connection = create_connection()

    if connection.is_connected():
        school_postal = "'%%'" if not args.get('schoolPostal', None) else f"'%{args.get('schoolPostal')}%'"
        query = f"select * from school_project_distance where schoolPostal like {school_postal}"
        print("query: ", query)
        logger.info(f"get properties by shcool query: {query}")
        cursor = connection.cursor()
        cursor.execute(query)
        column_names = [col[0] for col in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        # print("query result: ", data)
        connection.close()
        return data
    else:
        return "DB is not connected"


def get_property(args: dict):
    connection = create_connection()
    cursor = connection.cursor()

    if connection.is_connected():
        project_name = "''" if not args.get('projectName', None) else f"'{args.get('projectName')}'"
        availability_query = f"select sold_to_date as soldToDate, units_avail as unitsAvail " \
                             f"from private_project_sales where project = {project_name} limit 1"
        cursor.execute(availability_query)
        column_names = [col[0] for col in cursor.description]
        availability = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        availability = next(iter(availability)) if availability else {}
        logger.info(f"availability query: {availability_query}")

        transaction_query = f"select marketSegment, area, floorRange, noOfUnits, contractDate, typeOfSale, price, propertyType, district, typeOfArea, tenure, unitPrice " \
                            f"from private_project_transaction where project = {project_name}"
        cursor.execute(transaction_query)
        column_names = [col[0] for col in cursor.description]
        recent_tnx = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        # print("transaction_query: ", transaction_query)
        logger.info(f"transaction query: {transaction_query}")
        # print("query result: ", recent_tnx)

        price_history_query = f"select contractDate as timestamp, round(avg(unitPrice), 2) as unitPrice " \
                              f"from private_project_transaction where project = {project_name} " \
                              f"group by contractDate order by contractDate"
        cursor.execute(price_history_query)
        column_names = [col[0] for col in cursor.description]
        price_history = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        # print("price_history_query: ", price_history_query)
        logger.info(f"price history query: {price_history_query}")
        # print("query result: ", price_history)

        project_detail_query = f"select projectName, projectBlkPostal as postal, street, address, developerName " \
                               f"from school_project_distance where projectName = {project_name} limit 1"
        cursor.execute(project_detail_query)
        column_names = [col[0] for col in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        data = next(iter(data)) if data else {}
        data["recentTnx"] = recent_tnx
        data["priceHistory"] = price_history
        data["soldToDate"] = availability.get("soldToDate", "")
        data["unitsAvail"] = availability.get("unitsAvail", "")
        # print("project_detail_query: ", project_detail_query)
        logger.info(f"project details query: {project_detail_query}")
        # print("query result: ", data)
        connection.close()
        return data
    else:
        return "DB is not connected"


if __name__ == "__main__":
    get_schools()