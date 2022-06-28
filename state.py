from Code.Backend.Service.Objects.Configuration import *


def state(service):
    u1id = service.short_login(u1)
    u2id = service.short_login(u2)
    u3id = service.short_login(u3)
    u4id = service.short_login(u4)
    u5id = service.short_login(u5)
    store_name = "s1"
    store_id = service.short_open_store(u2id, store_name)
    r = service.add_new_product_to_inventory(u2id, store_id, 'Bamba', 'bla bla', 30, 'fruits')
    if r.error_occurred(): raise Exception(r.msg)
    bamba_id = r.value
    quantity = 20
    r = service.add_products_to_inventory(u2id, store_id, bamba_id, quantity)
    if r.error_occurred(): raise Exception(r.msg)
    r1 = service.add_store_manager(u2id, store_id, u3["username"])
    service.change_manager_permission(u2id, store_id, u3["username"],{1: True, 2: False, 3: True, 4: False, 5: False, 6: False, 7: False, 8:False, 9:False} )
    if r1.error_occurred(): raise Exception(
        "Error in add store owner")
    r = service.logout(u5id)
    if r.error_occurred(): raise Exception(r.msg)
