import csv
import json
from datetime import datetime, timedelta


def read_csv():
    with open("./invoice.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            data:dict = procces_data(row)
            data_json = json.dumps(data)
            print(data_json)



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
        return dict_data
    except Exception as e:
        print(e)


def cc_amount(row) -> dict:
    importe = float(row[10])
    return {"importe" : importe}


def cc_date(row) -> dict:
    fecha = row[6]
    return {"fechaVencimiento" : fecha}


def return_current_account(row)-> dict:
    dic_cc:dict = {}
    dic_cc.update(cc_date(row))
    dic_cc.update(cc_amount(row))
    return {
        "cuotasCuentaCorriente": [dic_cc]
    }

def perceptions_aliquot(row)-> dict:
    if row[19] != 0:
        return {"codigoAlicuota": int(row[17])}


def perceptions_code()-> dict:
    return {"codigoPercepcion": ""}


def perceptions_percentage(row)-> dict:
    porcentaje = float(row[18])
    return {"porcentaje": porcentaje}


def perceptions_base(row)-> dict:
    base = float(row[24])
    return {"base": base}


def perceptions_amount(row)-> dict:
    importe = float(row[24])
    return {"importe": importe}


def perceptions_aliquot_2(row)-> dict:
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
    else:
        return {"codigoAlicuota": "ERROR_(codigoAlicuota)"}

    return {"codigoAlicuota": (codigoAlicuota)}


def perceptions_code_2()-> dict:
    return {"codigoPercepcion": "AR"}


def perceptions_percentage_2(row)-> dict:
    porcentaje = float(row[21])
    return {"porcentaje": porcentaje}


def perceptions_base_2(row)-> dict:
    base = float(row[24])
    return {"base": base}


def perceptions_amount_2(row)-> dict:
    importe = float(row[22])
    return {"importe": importe}


def items_perceptions(row)-> dict:
    #if row[19] and row[22]:
    dic_perceptions: dict = {}
    dic_perceptions.update(perceptions_aliquot(row))
    dic_perceptions.update(perceptions_code())
    dic_perceptions.update(perceptions_percentage(row))
    dic_perceptions.update(perceptions_base(row))
    dic_perceptions.update(perceptions_amount(row))
    dic_perceptions_2: dict = {}
    dic_perceptions_2.update(perceptions_aliquot_2(row))
    dic_perceptions_2.update(perceptions_code_2())
    dic_perceptions_2.update(perceptions_percentage_2(row))
    dic_perceptions_2.update(perceptions_base_2(row))
    dic_perceptions_2.update(perceptions_amount_2(row))
    return {
        "percepciones": [dic_perceptions, dic_perceptions_2]
        } #TODO


def items_amount_iva(row) -> dict:
    if float(row[16]) != 0:
        importe = float(row[16])
    else:
        importe = 0
    return {"importeIva": importe }


def items_amount_without_taxes(row) -> dict:
    importe = float(row[24])
    return {"importeSinImpuestos": importe }


def items_amount(row) -> dict:
    precio = float(row[24]) + float(row[16])
    return {"importe": precio }


def items_price(row) -> dict:
    precio = float(row[24]) + float(row[16])
    return {"precio": precio }


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
        pass #TODO


def items_download_stock(row) -> dict:
    return  {"descargaStock": False}


def items_code(row) -> dict:
    code:str = row[23]
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
    dic_items.update(items_perceptions(row))
    dic_return = {
        "items": [dic_items]
    }

    return dic_return


def return_constant_dic() -> dict:
    return (
        {
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
    )


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
    dic: dict = {"totalSinImpuestos:": float(total_without_taxes)}
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
        "leyenda2": "Leyenda 2",
        "leyenda3": "Leyenda 3",
        "leyenda4": "Leyenda 4",
        "leyenda5": "Leyenda 5",
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
        "codigoDeposito": "1",
    }
    return dic


def code_list_price(row) -> dict:
    if client_code(row).get("codigoCliente") == "50007" or row[4] == "T":
        code_list_price = 1
    else:
        code_list_price = 11
    dic = {"codigoListaPrecio": code_list_price}
    return dic


def voucher_date(row) -> dict:
    date = datetime.strptime(row[3], "%d/%m/%y")
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
    dic = {"codigoCondicionDeVenta": row[13]}
    return dic


def client_code(row) -> dict:
    client_code = "{}{}".format("0", str(row[0]))
    dic = {"codigoCliente": client_code}  # TODO
    return dic


def voucher_code(row) -> dict:
    dic: dict = {}
    dic = {"codigoTalonario": "1"}  # TODO
    return dic


def number_voucher(row) -> dict:
    dic: dict = {}
    voucher_number = row[25].replace('"', "")
    dic = {"numeroComprobante": voucher_number}
    if len(row[25]) == 16:
        return dic
    return {"numeroComprobante": "ERROR"}


def code_type_voucher(row) -> dict:
    dic: dict = {}
    if row[1] == "FAC":
        dic = {"codigoTipoComprobante": "FAC"}
    elif row[1] == "CRE":
        dic = {"codigoTipoComprobante": "04"}
    elif row[1] == "DEB":
        dic = {"codigoTipoComprobante": "05"}
    return dic


read_csv()
