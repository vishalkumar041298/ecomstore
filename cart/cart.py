from decimal import Decimal

from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        # Returning user - obtain his/her existing session
        cart = self.session.get('session_key')
        # New user - generate a new session
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart
    
    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] += product_qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}
        self.session.modified = True
    
    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart.pop(product_id)     
        self.session.modified = True
    
    def update(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty
        self.session.modified = True

    def __len__(self):
        return sum([item['qty'] for item in self.cart.values()])
    
    def __iter__(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
    
    def get_total_price(self):
        return round(sum(Decimal(item['price']) * item['qty'] for item in self.cart.values()), 2)
