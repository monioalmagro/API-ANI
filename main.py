import csv
import json
from datetime import datetime, timedelta

import requests
from requests.structures import CaseInsensitiveDict


def read_csv():
    with open("./invoice.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            status, data = procces_data(row)
            if status:
                data_json = json.dumps(data)
                status_code = post_to_api(data_json)
                report(status, data, status_code)
            else:
                report(status, row, data)


def report(status, data, code=None):
    with open('logs.txt', 'a') as f:
        if code:
            log = "\n{}--{}--{}".format(str(status), str(data), str(code))
        else:
            log = "\n{}--{}--{}".format(str(status), str(code), str(data))
        f.write(log)


# +++++++++++++++++++++  POST TO API     +++++++++++++++++++++++++++++++++++++


def post_to_api(data):
    url = "http://desktop-l4fsbsj:17000/FacturadorVenta/registrar?"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["ApiAuthorization"] = "3612a301-3803-4593-91bd-abbd7f08b205"
    headers["Company"] = "1"

    resp = requests.post(url, headers=headers, data=data)

    return resp.status_code


# +++++++++++++++++++++++  PROCCES DATA    +++++++++++++++++++++++++++++++++++


def procces_data(row):
    dict_data: dict = {}
    try:
        dict_data.update(code_type_voucher(row))
        dict_data.update(number_voucher(row))
        dict_data.update(voucher_code(row))
        dict_data.update(client_code(row))
        dict_data.update(code_sale(row))
        dict_data.update(operation_code(row))
        dic, dic_2 = voucher_date(row)
        dict_data.update(dic)
        dict_data.update(dic_2)
        dict_data.update(code_list_price(row))
        dict_data.update(deposit_code(row))
        dict_data.update(vendor_code(row))
        dict_data.update(accounting_seat(row))
        dict_data.update(legend_1(row))
        dict_data.update(legend_2_to_5())
        dict_data.update(is_money_foreign(row))
        dict_data.update(quotation(row))
        dict_data.update(total_foreign_currency(row))
        dict_data.update(total(row))
        dict_data.update(total_without_taxes(row))
        dict_data.update(totally_exempt(row))
        dict_data.update(total_iva(row))
        dict_data.update(sub_total(row))
        dict_data.update(sub_total_without_taxes(row))
        dict_data.update(return_constant_dic())
        dict_data.update(returns_items(row))
        dict_data.update(return_current_account(row))
        return True, [dict_data]
    except Exception as error:
        return False , error


# +++++++++++++++++++  CURRENT ACCOUNT     +++++++++++++++++++++++++++++++++++


def cc_amount(row) -> dict:
    importe = float(row[10])
    return {"importe": importe}


def cc_date(row) -> dict:
    fecha = row[6]
    return {"fechaVencimiento": fecha}


def return_current_account(row) -> dict:
    dic_cc: dict = {}
    dic_cc.update(cc_date(row))
    dic_cc.update(cc_amount(row))
    return {"cuotasCuentaCorriente": [dic_cc]}


# ++++++++++++++++++++++  PERCEPTIONS     ++++++++++++++++++++++++++++++++++++


def perceptions_aliquot(row) -> dict:
    if row[19] != 0:
        return {"codigoAlicuota": int(row[17])}


def perceptions_code() -> dict:
    return {"codigoPercepcion": ""}


def perceptions_percentage(row) -> dict:
    porcentaje = float(row[18])
    return {"porcentaje": porcentaje}


def perceptions_base(row) -> dict:
    base = float(row[24])
    return {"base": base}


def perceptions_amount(row) -> dict:
    importe = float(row[19])
    return {"importe": importe}


def perceptions_aliquot_agip(row) -> dict:
    if float(row[21]) == 1.5:
        codigoAlicuota = 1
    if float(row[21]) == 2:
        codigoAlicuota = 2
    if float(row[21]) == 2.5:
        codigoAlicuota = 3
    if float(row[21]) == 3:
        codigoAlicuota = 4
    if float(row[21]) == 3.5:
        codigoAlicuota = 5
    if float(row[21]) == 4:
        codigoAlicuota = 6
    if float(row[21]) == 4.5:
        codigoAlicuota = 7
    if float(row[21]) == 5:
        codigoAlicuota = 8
    if float(row[21]) == 6:
        codigoAlicuota = 9
    if float(row[21]) == 0.1:
        codigoAlicuota = 10
    if float(row[21]) == 0.2:
        codigoAlicuota = 11
    if float(row[21]) == 0.3:
        codigoAlicuota = 12
    if float(row[21]) == 0.5:
        codigoAlicuota = 13
    if float(row[21]) == 1:
        codigoAlicuota = 14
    if float(row[21]) == 2.6:
        codigoAlicuota = 15
    if float(row[21]) == 2.7:
        codigoAlicuota = 16
    if float(row[21]) == 3.2:
        codigoAlicuota = 17
    if float(row[21]) == 0.01:
        codigoAlicuota = 18
    if float(row[21]) == 0.75:
        codigoAlicuota = 19

    return {"codigoAlicuota": (codigoAlicuota)}


def perceptions_code_agip() -> dict:
    return {"codigoPercepcion": "AR"}


def perceptions_percentage_agip(row) -> dict:
    porcentaje = float(row[21])
    return {"porcentaje": porcentaje}


def perceptions_base_agip(row) -> dict:
    base = float(row[24])
    return {"base": base}


def perceptions_amount_agip(row) -> dict:
    importe = float(row[22])
    return {"importe": importe}


def perceptions_arba(row) -> dict:
    # ARBA
    dic_perceptions_arba: dict = {}
    dic_perceptions_arba.update(perceptions_aliquot(row))
    dic_perceptions_arba.update(perceptions_code())
    dic_perceptions_arba.update(perceptions_percentage(row))
    dic_perceptions_arba.update(perceptions_base(row))
    dic_perceptions_arba.update(perceptions_amount(row))
    return dic_perceptions_arba


def perceptions_agip(row) -> dict:
    # AGIP
    dic_perceptions_agip: dict = {}
    dic_perceptions_agip.update(perceptions_aliquot_agip(row))
    dic_perceptions_agip.update(perceptions_code_agip())
    dic_perceptions_agip.update(perceptions_percentage_agip(row))
    dic_perceptions_agip.update(perceptions_base_agip(row))
    dic_perceptions_agip.update(perceptions_amount_agip(row))
    return dic_perceptions_agip


def items_perceptions(row):
    a = float(row[19])
    b = float(row[22])
    if a == 0 and b == 0:
        return None
    if a != 0 and b == 0:
        arba: dict = perceptions_arba(row)
        return {"percepciones": [arba]}
    if a == 0 and b != 0:
        agip: dict = perceptions_agip(row)
        return {"percepciones": [agip]}
    if a != 0 and b != 0:
        arba: dict = perceptions_arba(row)
        agip: dict = perceptions_agip(row)
        return {"percepciones": [arba, agip]}


# +++++++++++++++++++++++      ITEMS    ++++++++++++++++++++++++++++++++++++++


def items_amount_iva(row) -> dict:
    if float(row[16]) != 0:
        importe = float(row[16])
    else:
        importe = 0
    return {"importeIva": importe}


def items_amount_without_taxes(row) -> dict:
    importe = float(row[24])
    return {"importeSinImpuestos": importe}


def items_amount(row) -> dict:
    precio = float(row[24]) + float(row[16])
    return {"importe": precio}


def items_price(row) -> dict:
    precio = float(row[24]) + float(row[16])
    return {"precio": precio}


def items_code_um() -> dict:
    return {"codigoUM": "UNI"}


def items_deposit_code(row) -> dict:
    return {"codigoDeposito": "1"}


def items_quantity(row) -> dict:
    return {"cantidad": 1}


def items_rate_iva_code(row) -> dict:
    if row[16] != 0:
        return {"codigoTasaIva": "1"}
    else:
        pass  # TODO


##################################


def items_download_stock(row) -> dict:
    return {"descargaStock": False}


def items_code(row) -> dict:
    code: str = row[23]
    return {"codigo": code}


def returns_items(row) -> dict:
    dic_items: dict = {}
    dic_items.update(items_code(row))
    dic_items.update(items_download_stock(row))
    dic_items.update(items_rate_iva_code(row))
    dic_items.update(items_quantity(row))
    dic_items.update(items_deposit_code(row))
    dic_items.update(items_code_um())
    dic_items.update(items_price(row))
    dic_items.update(items_amount(row))
    dic_items.update(items_amount_without_taxes(row))
    dic_items.update(items_amount_iva(row))
    if items_perceptions(row):
        dic_items.update(items_perceptions(row))
    dic_return = {"items": [dic_items]}

    return dic_return


# ***********************  JSON        ***************************************


def return_constant_dic() -> dict:
    return {
        "descuentoPorcentaje": 0,
        "descuentoMonto": 0,
        "descuentoMontoSinIva": 0,
        "recargoPorcentaje": 0,
        "recargoMonto": 0,
        "recargoMontoSinIva": 0,
        "recargoFletePorcentaje": 0,
        "recargoFleteMonto": 0,
        "recargoFleteMontoSinIva": 0,
        "interesesPorcentaje": 0,
        "interesesMontoSinIva": 0.00,
        "observaciones": "",
        "rg3668TipoIdentificacionFirmante": None,
        "rg3668CaracterDelFirmante": None,
        "rg3668CodigoIdentificacionFirmante": "",
        "rg3668MotivoDeExcepcion": None,
        "rg3668CodigoWeb": "666",
    }


def sub_total_without_taxes(row) -> dict:
    sub_total_without_taxes = float(row[7]) + float(row[9])
    dic: dict = {"subtotalSinImpuestos": sub_total_without_taxes}
    return dic


def sub_total(row) -> dict:
    sub_total = float(row[7]) + float(row[9]) + float(row[8])
    dic: dict = {"subtotal": sub_total}
    return dic


def total_iva(row) -> dict:
    total_iva = row[8]
    dic: dict = {"totalIva": float(total_iva)}
    return dic


def totally_exempt(row) -> dict:
    totally_exempt = row[9]
    dic: dict = {"totalExento": float(totally_exempt)}
    return dic


def total_without_taxes(row) -> dict:
    total_without_taxes = row[7]
    dic: dict = {"totalSinImpuestos": float(total_without_taxes)}
    return dic


def total(row) -> dict:
    total = row[10]
    dic: dict = {"total": float(total)}
    return dic


def total_foreign_currency(row) -> dict:
    total_foreign_currency = row[11]
    dic: dict = {"totalmonedaextranjera": float(total_foreign_currency)}
    return dic


def quotation(row) -> dict:
    quotation = row[5]
    dic: dict = {"cotizacion": float(quotation)}
    return dic


def is_money_foreign(row) -> dict:
    if row[4] == "T" or int(client_code(row).get("codigoCliente")) >= 50007:
        is_money_foreign: bool = False
    else:
        is_money_foreign: bool = True
    dic: dict = {"esMonedaExtranjera": is_money_foreign}
    return dic


def legend_2_to_5() -> dict:
    return {
        "leyenda2": None,
        "leyenda3": None,
        "leyenda4": None,
        "leyenda5": None,
    }


def legend_1(row) -> dict:
    legend = row[2]
    dic: dict = {"leyenda1": legend}
    return dic


def accounting_seat(row) -> dict:
    accounting_seat = row[12].replace('"', "")
    dic: dict = {
        "codigoAsiento": accounting_seat,
    }
    return dic


def vendor_code(row) -> dict:
    list_vendor_code: list = [
        "01L E",
        "01L I",
        "02L E",
        "02L I",
        "03L E",
        "04L E",
        "05L E",
        "06L E",
        "07L E",
        "08L E",
        "097L E",
        "09L E",
        "107L E",
        "10L E",
    ]
    client_code_s = int(client_code(row).get("codigoCliente"))
    if client_code_s >= 10001 and client_code_s <= 10017:
        if row[23] in list_vendor_code:
            vendor_code = "02"
        else:
            vendor_code = "01"
    else:
        vendor_code = "01"
    dic: dict = {"codigoVendedor": vendor_code}
    return dic


def deposit_code(row) -> dict:
    dic: dict = {
        "codigoDeposito": " 1",
    }
    return dic


def code_list_price(row) -> dict:
    if client_code(row).get("codigoCliente") == "50007" or row[4] == "T":
        code_list_price = "1"
    else:
        code_list_price = "11"
    dic = {"codigoListaPrecio": code_list_price}
    return dic


def voucher_date(row) -> dict:
    date = datetime.strptime(row[3], "%d/%m/%Y")
    iso_date = date.isoformat()
    one_day_before = date - timedelta(days=1)
    one_day_before_iso = one_day_before.isoformat()
    dic = {"fechaComprobante": iso_date}
    dic_2 = {"fechaCierreTesoreria": one_day_before_iso}
    return dic, dic_2


def operation_code(row) -> dict:
    dic: dict = {}
    if row[8] == 0:
        operation_code = "0"
    else:
        operation_code = "A"
    dic = {"codigoOperacionRG3685": operation_code}
    return dic


def code_sale(row) -> dict:
    dic: dict = {}
    dic = {"codigoCondicionDeVenta": int(row[13])}
    return dic


def client_code(row) -> dict:
    client_code = "{}{}".format(str(row[0]), " ")
    dic = {"codigoCliente": client_code}
    return dic


def voucher_code(row) -> dict:
    talonario = row[25]
    letra = talonario[0]
    pv = talonario[1:6]
    tcomp = row[1]
    
    if tcomp == "FAC" and letra == "A" and pv == "00003":
        talonario = 90

    if tcomp == "FAC" and letra == "A" and pv == "00010":
        talonario = 80

    if tcomp == "FAC" and letra == "A" and pv == "00014":
        talonario = 70

    if tcomp == "FAC" and letra == "A" and pv == "00017":
        talonario = 180

    if tcomp == "FAC" and letra == "A" and pv == "00018":
        talonario = 170

    if tcomp == "FAC" and letra == "A" and pv == "00019":
        talonario = 190

    if tcomp == "FAC" and letra == "B" and pv == "00003":
        talonario = 91

    if tcomp == "FAC" and letra == "B" and pv == "00010":
        talonario = 81

    if tcomp == "FAC" and letra == "B" and pv == "00014":
        talonario = 71

    if tcomp == "FAC" and letra == "B" and pv == "00017":
        talonario = 181

    if tcomp == "FAC" and letra == "B" and pv == "00018":
        talonario = 171

    if tcomp == "FAC" and letra == "E" and pv == "00006":
        talonario = 96

    if tcomp == "FAC" and letra == "E" and pv == "00013":
        talonario = 76

    if tcomp == "CRE" and letra == "A" and pv == "00009":
        talonario = 62

    if tcomp == "CRE" and letra == "A" and pv == "00010":
        talonario = 82

    if tcomp == "CRE" and letra == "A" and pv == "00014":
        talonario = 72

    if tcomp == "CRE" and letra == "A" and pv == "00003":
        talonario = 94

    if tcomp == "CRE" and letra == "A" and pv == "00017":
        talonario = 182

    if tcomp == "CRE" and letra == "A" and pv == "00018":
        talonario = 172

    if tcomp == "CRE" and letra == "A" and pv == "00019":
        talonario = 192

    if tcomp == "CRE" and letra == "B" and pv == "00010":
        talonario = 83

    if tcomp == "CRE" and letra == "B" and pv == "00014":
        talonario = 73

    if tcomp == "CRE" and letra == "B" and pv == "00017":
        talonario = 183

    if tcomp == "CRE" and letra == "B" and pv == "00018":
        talonario = 173

    if tcomp == "CRE" and letra == "E" and pv == "00006":
        talonario = 97

    if tcomp == "CRE" and letra == "E" and pv == "00013":
        talonario = 77

    if tcomp == "DEB" and letra == "A" and pv == "00003":
        talonario = 94

    if tcomp == "DEB" and letra == "A" and pv == "00019":
        talonario = 194

    if tcomp == "DEB" and letra == "A" and pv == "00010":
        talonario = 84

    if tcomp == "DEB" and letra == "A" and pv == "00014":
        talonario = 74

    if tcomp == "DEB" and letra == "A" and pv == "00017":
        talonario = 184

    if tcomp == "DEB" and letra == "A" and pv == "00018":
        talonario = 174

    if tcomp == "DEB" and letra == "A" and pv == "00009":
        talonario = 63

    if tcomp == "DEB" and letra == "B" and pv == "00010":
        talonario = 85

    if tcomp == "DEB" and letra == "B" and pv == "00014":
        talonario = 75

    if tcomp == "DEB" and letra == "B" and pv == "00017":
        talonario = 185

    if tcomp == "DEB" and letra == "B" and pv == "00018":
        talonario = 175

    if tcomp == "DEB" and letra == "E" and pv == "00006":
        talonario = 98

    if tcomp == "DEB" and letra == "E" and pv == "00013":
        talonario = 78

    return {"codigoTalonario": str(talonario)}  # TODO


def number_voucher(row) -> dict:
    dic: dict = {}
    voucher_number = row[25][:14]
    dic = {"numeroComprobante": voucher_number}
    return dic


def code_type_voucher(row) -> dict:
    dic: dict = {}
    if row[1] == "FAC":
        dic = {"codigoTipoComprobante": "FAC"}
    elif row[1] == "NC":
        dic = {"codigoTipoComprobante": "04"}
    elif row[1] == "ND":
        dic = {"codigoTipoComprobante": "05"}
    return dic


read_csv()
