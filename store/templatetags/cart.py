from django import template
register= template.Library()

@register.filter(name='is_in_cart') #find product is in the cart or not
def is_in_cart(product,cart):
    keys=cart.keys()
    for id in keys:
        if id.isdigit():
            if int(id) == product.id:   
                return True
    return False
        #print(product.id,id)
        #print(type(product.id),type(id))    


@register.filter(name='quantity') #find product quantity 
def quantity(product,cart):
    keys=cart.keys()
    for id in keys:
        if id.isdigit():
            if int(id) == product.id:
                return cart.get(id)   
    return 0


@register.filter(name='price') #find product quantity 
def price(product,cart):
    return product.price * quantity(product,cart)



@register.filter(name='totalprice') #find product quantity 
def totalprice(product,cart):
    sum=0
    for p in product:
        sum=sum+price(p,cart)
    return sum


@register.filter(name='currency') #find product quantity 
def currency(number):
    return "$"+str(number)
