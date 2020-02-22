# ETL Data Warehouse Workshop

This is a repository for hands on project doing ETL jobs using the famous Sakila database schema.

This workshop assumes you already have access to standard Sakila database schema and data. If this is not true, please follow this instruction https://dev.mysql.com/doc/sakila/en/sakila-installation.html

## Create Star Schema

### Step 1: Create and Use New Database

1. Access to mysql client command line
   ```sql
   mysql -u masvent -pmasvent -h [your-db-host]
   ```
1. Create `sakila_dw_[yourname]` database
   ```sql
   mysql> create database sakila_dw_[yourname];
   ```
1. Use `sakila_dw_[yourname]` database
   ```sql
   mysql> use sakila_dw_[yourname];
   ```

### Step 2: Create `Date` Dimension

Run:

```sql
mysql> CREATE TABLE dimDate
(
    date_key integer NOT NULL,
    date date NOT NULL,
    year smallint NOT NULL,
    quarter tinyint NOT NULL,
    month tinyint NOT NULL,
    day tinyint NOT NULL,
    week tinyint NOT NULL,
    is_weekend boolean,
    is_holiday boolean,
    PRIMARY KEY(date_key)
);
```

### Step 3: Create `Customer` Dimension (SCD Type-2)

Run:

```sql
mysql> CREATE TABLE dimCustomer
(
    customer_key int NOT NULL AUTO_INCREMENT,
    customer_id smallint(5) unsigned NOT NULL,
    first_name varchar(45) NOT NULL,
    last_name varchar(45) NOT NULL,
    email varchar(50),
    address varchar(50) NOT NULL,
    address2 varchar(50),
    district varchar(20) NOT NULL,
    city varchar(50) NOT NULL,
    country varchar(50) NOT NULL,
    postal_code varchar(10),
    phone varchar(20),
    active tinyint(1) NOT NULL,
    create_date datetime NOT NULL,
    start_date date NOT NULL,
    end_date date,
    PRIMARY KEY(customer_key)
);
```

### Step 4: Create `Movie` Dimension (SCD Type-0)

```sql
mysql> CREATE TABLE dimMovie
(
    movie_key int NOT NULL AUTO_INCREMENT,
    film_id smallint(5) unsigned NOT NULL,
    title varchar(255) NOT NULL,
    description text,
    release_year year(4),
    language varchar(20) NOT NULL,
    original_language varchar(20),
    rental_duration tinyint(3) unsigned NOT NULL,
    length smallint(5) unsigned NOT NULL,
    rating varchar(5) NOT NULL,
    special_features varchar(60) NOT NULL,
    PRIMARY KEY (movie_key)
);
```

### Step 5: Create `Store` Dimension (SCD Type-2)

Run:

```sql
CREATE TABLE dimStore
(
    store_key int NOT NULL AUTO_INCREMENT,
    store_id smallint(5) unsigned NOT NULL,
    address varchar(50) NOT NULL,
    address2 varchar(50),
    district varchar(20) NOT NULL,
    city varchar(50) NOT NULL,
    country varchar(50) NOT NULL,
    postal_code varchar(10),
    manager_first_name varchar(45) NOT NULL,
    manager_last_name varchar(45) NOT NULL,
    start_date date NOT NULL,
    end_date date,
    PRIMARY KEY (store_key)
);
```

### Step 6: Create `Sales` Fact

Run:

```sql
mysql> CREATE TABLE factSales
(
    sales_key INT NOT NULL AUTO_INCREMENT,
    date_key INT NOT NULL,
    customer_key INT NOT NULL,
    movie_key INT,
    store_key INT,
    sales_amount decimal(5,2) NOT NULL,
    FOREIGN KEY fk_date (date_key) REFERENCES dimDate(date_key),
    FOREIGN KEY fk_customer (customer_key) REFERENCES dimCustomer(customer_key),
    FOREIGN KEY fk_movie (movie_key) REFERENCES dimMovie(movie_key),
    FOREIGN KEY fk_store (store_key) REFERENCES dimStore(store_key),
    PRIMARY KEY (sales_key)
);
```

## Run ETL Jobs

### Step 1: Install pre-requisite

1. Install Python 3
2. Install `pip`
3. Install Git


### Step 2: Clone Git Repository

```
git clone https://github.com/asatrya/ETL-DataWarehouse-Workshop
```

### Step 3: Install Dependencies

```sh
pip install -r requirements.txt
```

### Step 4: Edit Configuration

Edit your credentials in `conf/.env`

### Step 5: Run Job

```bash
python jobs/etl_dim_customer.py
python jobs/etl_dim_movie.py
python jobs/etl_dim_store.py
python jobs/generate_dim_date.py
python jobs/etl_fact_sales.py
```

## Answer Some Business Questions

How much sales did we do, by store and by month?
