# Asystent AI dla Testera Oprogramowania
Jest to prosta aplikacja webowa z interfejsem która wykorzystuje framework **Flask** wraz z **API Gemini 2.0** aby umożliwić testerom oprogramowania otrzymanie
pomocy z np. 
1. Testowaniem kodu pod względem naruszania zasad SOLID, prawa Demeter oraz sprawdzaniem jakości kodu. 
2. Generowaniem testów jednostkowych na podstawie kodu,
3. Generowaniem przypadków testowych dla opisanej funkcjonalności
Aplikacja zawiera także opcję wybierania języków(angielski i polski) co zmienia prompt, oraz wybór między krótką i zwięzłą odpowiedzią AI a długą, szczegółową.
Autor: Szymon Masłoń
## Przykładowe testy

### TEST FOR SOLID
#### Prompt
```
class Order:
    def __init__(self, id, items, customer):
        self.id = id
        self.items = items
        self.customer = customer


class OrderProcessor:
    def __init__(self, order):
        self.order = order

    def process_order(self):
        self._validate_order()
        self._save_order_to_database()
        self._send_confirmation_email()

    def _validate_order(self):
        print("Walidacja zamowienia.")

    def _save_order_to_database(self):
        print("Zapisywanie zamowienia do bazy danych.")

    def _send_confirmation_email(self):
        print("Wysylanie e-maila potwierdzajacego.")


order = Order("123", ["Produkt A", "Produkt B"], "Jan Kowalski")
processor = OrderProcessor(order)
processor.process_order()
```
#### Rezultat
![](https://github.com/Mevss/TIJO_Asystent/blob/main/img/1.png)

### UNIT TEST
#### Prompt
```
class ShoppingCart:
    def __init__(self):
        self.products = {}
        self.discount = 0
        self.checked_out = False

    def add_product(self, product_name: str, price: int, quantity: int) -> bool:
        if product_name in self.products:
            return False
        self.products[product_name] = {'price': price, 'quantity': quantity}
        return True

    def remove_product(self, product_name: str) -> bool:
        if product_name in self.products:
            del self.products[product_name]
            return True
        return False

    def update_quantity(self, product_name: str, new_quantity: int) -> bool:
        if product_name in self.products:
            self.products[product_name]['quantity'] = new_quantity
            return True
        return False

    def get_products(self):
        return list(self.products.keys())

    def count_products(self) -> int:
        return len(self.products)

    def get_total_price(self) -> int:
        total = sum(p['price'] * p['quantity'] for p in self.products.values())
        if self.discount > 0:
            total = int(total * (1 - self.discount / 100))
        return total

    def apply_discount_code(self, discount_code: str) -> bool:
        valid_codes = {'SAVE10': 10, 'SAVE20': 20}
        if discount_code in valid_codes:
            self.discount = valid_codes[discount_code]
            return True
        return False

    def checkout(self) -> bool:
        if not self.products:
            return False
        self.checked_out = True
        return True

```
#### Rezultat
![](https://github.com/Mevss/TIJO_Asystent/blob/main/img/2.png)


### TEST CASES
#### Prompt
```
function calculateAge(birthDate, currentDate = new Date()) {

    if (!birthDate) {
        throw new Error("Data urodzenia jest wymagana");
    }
    
    const birth = new Date(birthDate);
    const current = new Date(currentDate);
    
    if (birth > current) {
        throw new Error("Data urodzenia nie może być w przyszłości");
    }
    
    let age = current.getFullYear() - birth.getFullYear();
    const monthDiff = current.getMonth() - birth.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && current.getDate() < birth.getDate())) {
        age--;
    }
    
    return age;
}
```
#### Rezultat
![](https://github.com/Mevss/TIJO_Asystent/blob/main/img/3.png)
