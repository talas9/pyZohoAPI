# This file is part of pyZohoAPI, Copyright (C) Todd D. Esposito 2021.
# Distributed under the MIT License (see https://opensource.org/licenses/MIT).

from pyzohoapi.objecttypes.mixins.CompositeItemOps import HasBundle
from ..core import ZohoObjectBase
from .mixins import HasActivate, HasAddresses, HasConfirm, HasCustomFields, HasDelivered, HasDraft, HasImage, HasVoid


def ZohoObjectFactory(name,
    urlPath=None, responseKey=None, pluralResponseKey=None,
    idKey=None, numberKey=None, raw=False,
    mixins=[]):
    """ Factory function to create a Zoho Object type

    Unless overridden by the optional parameters, `name` is used to determine how
    Zoho API objects are accessed and parsed.

    * The URL used will be https:/{api-root}/{pluralized `name` -or- `urlPath`}
    * A list of objects is under the JSON key `pluralizedResponseKey` -or- `responseKey` pluralized -or- `name` pluralized
    * A single object is under the JSON key `responseKey` -or- `name`
    * The object ID is under the JSON key `idKey` -or- `{name}_id`
    * The object Number is under the JSON key `numberKey` -or- `{name}_number`

    :param name: object-class name; the basis of the API URL path unless overridden.
    :param urlPath: sets th API URL path
    :param responseKey: sets the singular (and maybe plural) response key(s).
    :param pluralResponseKey: sets the plural response key.
    :param idKey: sets the id field key.
    :param numberKey: sets the number field key.
    :param raw: handle the response body as raw data rather than json for non-list responses
    :param mixins: list of object-type mixins. Defaults to [].
    :return: ZohoObject sub-class
    """
    return type(name, tuple([ZohoObjectBase] + mixins), {
        '__name__': name,
        '_type': urlPath if urlPath else f"{name.lower()}s",
        '_singular': responseKey if responseKey else name.lower(),
        '_plural': pluralResponseKey if pluralResponseKey else f"{responseKey}s" if responseKey else f"{name.lower()}s",
        '_id_field': idKey if idKey else f"{name.lower()}_id",
        '_number_field': numberKey if numberKey else f"{name.lower()}_number",
        '_is_raw': raw,
    })

Account = ZohoObjectFactory("ChartOfAccount", idKey="account_id")
Bill = ZohoObjectFactory("Bill", mixins=[HasCustomFields])
Brand = ZohoObjectFactory("Brand")
Bundle = ZohoObjectFactory("Bundle")
CompositeItem = ZohoObjectFactory("CompositeItem",
    responseKey="composite_item", idKey="composite_item_id",
    mixins=[HasActivate, HasBundle, HasCustomFields])
Contact = ZohoObjectFactory("Contact", mixins=[HasActivate, HasAddresses, HasCustomFields])
CreditNote = ZohoObjectFactory("CreditNode", mixins=[HasCustomFields])
Currency = ZohoObjectFactory("Currency", urlPath="settings/currencies",
    pluralResponseKey="currencies")
CustomerPayment = ZohoObjectFactory("CustomerPayment",
    idKey="payment_id", numberKey="payment_number", mixins=[HasCustomFields])
Document = ZohoObjectFactory("Document", raw=True)
Invoice = ZohoObjectFactory("Invoice", mixins=[HasCustomFields])
Item = ZohoObjectFactory("Item", mixins=[HasActivate, HasCustomFields, HasImage])
ItemAdjustment = ZohoObjectFactory("ItemAdjustment",
    urlPath="inventoryadjustments", responseKey="inventory_adjustment",
    idKey="inventory_adjustment_id")
ItemGroup = ZohoObjectFactory("ItemGroup", idKey="group_id",
    responseKey="group", mixins=[HasActivate])
Organization = ZohoObjectFactory("Organization")
Package = ZohoObjectFactory("Package", mixins=[HasCustomFields])
PriceList = ZohoObjectFactory("PriceList", urlPath="pricebooks",
    responseKey="pricebook", idKey="pricebook_id",
    mixins=[HasActivate])
PurchaseOrder = ZohoObjectFactory("PurchaseOrder", mixins=[HasCustomFields])
PurchaseReceive = ZohoObjectFactory("PurchaseReceive", mixins=[HasCustomFields])
RetainerInvoice = ZohoObjectFactory("RetainerInvoice", mixins=[HasDraft, HasVoid])
SalesOrder = ZohoObjectFactory("SalesOrder",
    mixins=[HasConfirm, HasCustomFields, HasVoid])
SalesPerson = ZohoObjectFactory("SalesPerson")
SalesReturn = ZohoObjectFactory("SalesReturn")
ShipmentOrder = ZohoObjectFactory("ShipmentOrder",
    responseKey="shipmentorder", idKey="shipment_id",
    numberKey="shipment_number", mixins=[HasCustomFields, HasDelivered])
Tax = ZohoObjectFactory("Tax", urlPath="settings/taxes",
    pluralResponseKey="taxes")
TaxAuthority = ZohoObjectFactory("Tax", urlPath="settings/taxauthorities",
    responseKey="tax_authority", pluralResponseKey="tax_authorities",
    idKey="tax_authority_id")
TaxExemption = ZohoObjectFactory("Tax", urlPath="settings/taxexemptions",
    responseKey="tax_exemption", idKey="tax_exemption_id")
TaxGroup = ZohoObjectFactory("Tax", urlPath="settings/taxgroups",
    responseKey="tax_group", idKey="tax_group_id")
TransferOrder = ZohoObjectFactory("TransferOrder",
    responseKey="transfer_order",
    idKey="transfer_order_id", numberKey="transfer_order_number")
User = ZohoObjectFactory("User", mixins=[HasActivate, HasCustomFields])
Warehouse = ZohoObjectFactory("Warehouse", urlPath="settings/warehouses",
    mixins=[HasActivate])
