# Група 7 - Наплата / сметки

## Студенти:

```
195094 - Божидар Спирковски
195063 - Мартин Трајковски
173274 - Виктор Божиновски
191178 - Симона Дрецкоска
```

## Микросервис:

наплата / сметки

## Краток опис:

Микросервис кој овозможува извршување на трансакции за услугите и производите како и чување на сметки.
Пристап до овој микросервис во рамките на апликацијата имаат самите вработени на центарот за згрижување на кучиња, како и самиот корисник кој креирал кориснички профил. Покрај основната фукнција за наплата, микросервисот овозможува корисникот да остави донација.
Преку сервисот корисникот ќе има детален преглед на услугите кои ги користел и цената на чинење на истите, преку генерираната сметка.
Бизнис кориснички сценарија:
Извршување на наплата
Принтање фактури
Детален приказ на услугите кои се наплатени
Начин на извршување на трансакција
Креирање на дневен извештај

## Од кој зависиме:

- Корисници
- Payment Gateway

## Кој зависи од нас:

- вршење услуги (козметички, ветеринарни, шетање) микросервисот
- чување на кучиња (ресурси, закажување)
- Продавница
- Вдомување / Наоѓање

## Функции

```
Функција pay:
    Права: Client, Employee, Admin
    Влезни атрибути: userId, shoppingCartId
    Влезни атрибути: userId, petId, serviceIds, price
    Влезни атрибути: userId, petId, resourceIds, price
    Излезни атрибути: Response.Status statusCode
    Преку оваа функција се плаќа со картичка, ја корити функцијата “create”, кога трансакцијата е успешна и парите се префрлени се сетира TransactionStatus на RESOLVED
```

```
Функција create:
    Права: Employee, Admin
    Влезни атрибути: userId, shoppingCartId
    Влезни атрибути: userId, petId, serviceIds, price
    Влезни атрибути: userId, petId, resourceIds, price
    Излезни атрибути: Transaction
```

```
Функција createInvoice:
    Права: Client, Employee, Admin
    Влезни атрибути: userId, shoppingCartId, serviceIds, resourceIds
    Излезни атрибути: void
```

```
Функција findAll:
    Права: Employee, Admin
    Влезни атрибути: /
    Излезни атрибути: List<Transaction>
```

```
Функција findById:
    Права: Employee, Admin
    Влезни атрибути: transactionId
    Излезни атрибути: Transaction
```

```
Функција findAllByCreatedAt:
    Права: Employee, Admin
    Влезни атрибути: /
    Излезни атрибути: List<Transaction>
```

```
Функција findAllByUserId:
    Права: Employee, Admin
    Влезни атрибути: userId
    Излезни атрибути: List<Transaction>
```

```
Функција setTranscationStatus:
    Права: Admin, functions
    Влезни атрибути: transactionId, status
    Излезни атрибути: bool
```

```
Функција cancelTransaction:
    Права: Admin, Employee
    Влезни атрибути: transactionId
    Излезни атрибути: bool
Преку оваа функција се плаќа со картичка, ја корити функцијата “create”, кога трансакцијата е успешна и парите се префрлени се сетира TransactionStatus на RESOLVED
```

```
Функција getDailyReportForDate:
    Права: Admin
    Влезни атрибути: date
    Излезни атрибути: DailyReport
    Прави некое query за дневен извештај во зависност од моделот DailyReport
```

## Модели

- **Класи**

```
enum TransactionStatus {
PENDING, RESOLVED, CANCELED
}

class Transaction {
Long id;
Long userId;
Date createdAt;
BigDecimal price;
TransactionStatus status;
String type;
}

class ServiceTransaction extends Transaction {
    Long petId;
    List<Long> serviceIds;
}

class ResourceTransaction extends Transaction {
Long petId;
    List<Long> resourceIds;
}

class MarketTransaction extends Transaction {
Long shoppingCartId;
}

class DailyReport {
    Date date;
    Long totalTransactions;
    Long totalResolved;
    Long totalPending;
    Long totalCanceled;
    BigDecimal totalPrice;
}
```

- **База**

```
transactions: id, userId, price, status
resource_transactions: id -> transactions.id, petId
service_transactions: id -> transactions.id, petId
market_transactions: id -> transactions.id, shoppingCartId
transactions_resources_services: id -> transactions.id, data_id
```

# Build

```
python -m virtualenv venv
./venv/Scripts/activate
pip install -r requirements.txt
python server.py
```

or

```
docker build -t payment-app .
docker run payment-app
```
