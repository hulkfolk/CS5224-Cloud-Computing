import pandas as pd
from geopy.distance import geodesic
import datetime


def calculate_distance() -> dict:
    schools = pd.read_csv("PrimarySchool.csv").to_dict()

    # {"AMBER 45": [(' POSTAL', ' BLK_NO', 'LATITUDE', ' LONGITUDE'), (' POSTAL', ' BLK_NO', 'LATITUDE', ' LONGITUDE')],
    #  "19 NASSIM": [(' POSTAL', ' BLK_NO', 'LATITUDE', ' LONGITUDE')]}
    projects = pd.read_csv("AllProjects.csv", sep='|').fillna('').groupby('project')[' POSTAL', ' BLK_NO', 'LATITUDE', ' LONGITUDE', 'street', 'developerName', ' ADDRESS'] \
        .apply(lambda g: list(map(tuple, g.values.tolist())))\
        .to_dict()


    output = []
    for row_num, postal in schools['postal_code'].items():
        school_latitude = schools['latitude'][row_num]
        school_longitude = schools['longitude'][row_num]

        for project, blks in projects.items():
            # each project generates at most two rows, blks within 1km and blks within 2km
            blk_within_1km = {}
            blk_within_2km = {}
            for blk in blks:
                pjt_latitude = blk[2]
                pjt_longitude = blk[3]
                distance = round(geodesic((school_latitude, school_longitude), (pjt_latitude, pjt_longitude)).kilometers, 2)
                if distance <= 1:
                    blk_within_1km['schoolPostal'] = postal
                    blk_within_1km['schoolName'] = schools['school_name'][row_num]
                    blk_within_1km['projectName'] = project
                    blk_within_1km['projectBlkPostal'] = blk[0]
                    blk_within_1km['projectBlkNum'] = blk_within_1km.get('projectBlkNum', '') + f'{blk[1]},'
                    blk_within_1km['projectBlkLatitude'] = blk[2]
                    blk_within_1km['projectBlkLongitude'] = blk[3]
                    blk_within_1km['street'] = blk[4]
                    blk_within_1km['developerName'] = blk[5]
                    blk_within_1km['address'] = blk[6]
                    blk_within_1km['distance'] = distance
                if 1 < distance <= 2:
                    blk_within_2km['schoolPostal'] = postal
                    blk_within_2km['schoolName'] = schools['school_name'][row_num]
                    blk_within_2km['projectName'] = project
                    blk_within_2km['projectBlkPostal'] = blk[0]
                    blk_within_2km['projectBlkNum'] = blk_within_1km.get('projectBlkNum', '') + f'{blk[1]},'
                    blk_within_2km['projectBlkLatitude'] = blk[2]
                    blk_within_2km['projectBlkLongitude'] = blk[3]
                    blk_within_2km['street'] = blk[4]
                    blk_within_2km['developerName'] = blk[5]
                    blk_within_2km['address'] = blk[6]
                    blk_within_2km['distance'] = distance
            if blk_within_1km:
                output.append(blk_within_1km)
            if blk_within_2km:
                output.append(blk_within_2km)

    # define columns
    schoolPostal = {}
    schoolName = {}
    projectName = {}
    projectBlkNum = {}
    projectBlkPostal = {}
    projectBlkLatitude = {}
    projectBlkLongitude = {}
    street = {}
    developerName = {}
    address = {}
    distance = {}  # 3 types of distance, <=1, 1-2, >2
    for i in range(0, len(output)):
        schoolPostal[i] = output[i]['schoolPostal']
        schoolName[i] = output[i]['schoolName']
        projectName[i] = output[i]['projectName']
        projectBlkPostal[i] = output[i]['projectBlkPostal']
        projectBlkNum[i] = output[i]['projectBlkNum']
        projectBlkLatitude[i] = output[i]['projectBlkLatitude']
        projectBlkLongitude[i] = output[i]['projectBlkLongitude']
        street[i] = output[i]['street']
        developerName[i] = output[i]['developerName']
        address[i] = output[i]['address']
        distance[i] = output[i]['distance']

    ret = {}
    ret['schoolPostal'] = schoolPostal
    ret['schoolName'] = schoolName
    ret['projectName'] = projectName
    ret['projectBlkPostal'] = projectBlkPostal
    ret['projectBlkNum'] = projectBlkNum
    ret['projectBlkLatitude'] = projectBlkLatitude
    ret['projectBlkLongitude'] = projectBlkLongitude
    ret['street'] = street
    ret['developerName'] = developerName
    ret['address'] = address
    ret['distance'] = distance
    return ret


def clean_transactions() -> dict:
    TYPE_OF_SALE_CODES = {1: "New Sale", 2: "Sub Sale", 3: "Resale"}
    SM_TO_SFT = 10.7639
    transactions = pd.read_csv("PrivateProjectTransactions_.csv", sep='|').to_dict()
    type_of_sale = transactions["typeOfSale"]
    contract_date = transactions["contractDate"]
    area = transactions["area"]
    price = transactions["price"]
    unit_price = {}

    for row, dt in contract_date.items():
        area[row] = round(area[row]*SM_TO_SFT, 2)
        unit_price[row] = round(price[row]/area[row], 2)
        contract_date[row] = datetime.datetime.strptime(str(dt).zfill(4), '%m%y').strftime('%Y-%m-%dT%H:%M:%S.%f')
        type_of_sale[row] = TYPE_OF_SALE_CODES[type_of_sale[row]]

    transactions["contractDate"] = contract_date
    transactions["unitPrice"] = unit_price
    return transactions


def write_to_csv(d: dict, file_name: str):
    df = pd.DataFrame.from_dict(d)
    df.to_csv(file_name, sep='|', index=False)


def clean_csv():
    schools = pd.read_csv("SchoolProjectDistance.csv", sep='|')
    schools.to_csv("SchoolProjectDistance_comma.csv", index=False)


if __name__ == "__main__":
    # write_to_csv(calculate_distance(), 'SchoolProjectDistance.csv')
    clean_csv()