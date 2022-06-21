from Code.Backend.Service.Objects.Configuration import *


def state(service):
    u1id = service.__short_login(u1)
    u2id = service.__short_login(u2)
    u3id = service.__short_login(u3)
    u4id = service.__short_login(u4)
    u5id = service.__short_login(u5)
    store_name = "s1"
    store_id = service.__short_open_store(u2id, store_name)
    Bamba = "Bamba"
    p_bamba = service(Bamba, 30)
    r = service.add_new_product_to_inventory(u2id, store_id, **p_bamba)
    if r.error_occurred(): raise Exception(r.msg)
    bamba_id = r.value
    quantity = 30
    r = service.add_products_to_inventory(u2id, store_id, bamba_id, quantity)
    if r.error_occurred(): raise Exception(r.msg)
    r1 = service.add_store_owner(u2id, store_id, u3["username"])
    r2 = service.add_store_owner(u2id, store_id, u4["username"])
    r3 = service.add_store_owner(u2id, store_id, u5["username"])
    if r1.error_occurred() or r2.error_occurred() or r3.error_occurred(): raise Exception(
        "Error in add store owner")
    r = service.logout(u5id)
    if r.error_occurred(): raise Exception(r.msg)
