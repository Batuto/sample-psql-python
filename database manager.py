#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
import logging
from pprint import pprint
from os import system
import sys


def connection():
    dbname = raw_input("Introduzca el nombre de la base de datos: ")
    user = raw_input("Introduzca el nombre de usuario: ")
    pwd = 'password'
    host = raw_input("Introduzca el host: ")
    try:
        db_usr = "dbname={0} user={1} host={2} password={3}".format(
            dbname, user, host, pwd)
        conn = psycopg2.connect(db_usr)
    except Exception:
        pprint("Error:")
        logging.basicConfig(format="%(message)s")
        logging.warning("Unable to connect")
        sys.exit(1)
    return conn

def create_tables():
    conn = connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE producto(producto_id int, primary key(producto_id), nombre varchar(50), departamento_id int, descripcion text, perecedero bool, proveedor_id int, precio_compra float, precio_venta float);")
    cur.execute("CREATE TABLE departamento(departamento_id int, primary key(departamento_id), nombre varchar(20));")
    cur.execute("CREATE TABLE proveedor(proveedor_id int, primary key(proveedor_id), nombre varchar(30), telefono char(10));")
    conn.commit()
    sys.exit()

def main():
    while True:
        conn = connection()
        cur = conn.cursor()
        system('clear')
        opcion = int(raw_input(
            """Introduzca su selección a desplegar:
            1 - Productos agrupados por vendedor.
            2 - Proveedores que proveen un determinado producto.
            3 - Departamento asignado a un producto.
            4 - Proveedores que proveen a un determinado departamento.
            5 - Los productos en un departamento.
            6 - Los prodcutos agrupados por departamento.
            7 - Los productos peredeceros en un departamento determinado.
            8 - Los proveedores que proveen productos perecederos.
            9 - La cantidad de productos que provee un proveedor."""
        ))
        opcion_dict = {
            1: "SELECT producto.nombre as Nombre, proveedor.nombre as Proveedor from producto join proveedor on producto.proveedor_id=proveedor.proveedor_id group by proveedor.nombre, producto.nombre;",
            2: "SELECT proveedor.nombre as Proveedor from producto join proveedor on producto.proveedor_id=proveedor.proveedor_id WHERE producto.nombre={};".format(raw_input("Introduzca el nombre de producto a buscar: ")),
            3: "SELECT departamento.nombre as Departamento from producto join departamento on producto.departamento_id=departamento.departamento_id WHERE producto.nombre={};".format(raw_input("Introduzca el nombre de producto a buscar: ")),
            4: "SELECT proveedor.nombre as Proveedor from producto join proveedor on producto.proveedor_id=proveedor.proveedor_id join departamento on producto.departamento_id=departamento.departamento_id where departamento.nombre={};".format(raw_input("Introduzca el nombre de departamento a buscar: ")),
            5: "SELECT producto.nombre as Producto from producto join departamento on producto.departamento_id=departamento.departamento_id WHERE departamento.nombre={};".format(raw_input("Introduzca el nombre de departamento a buscar: ")),
            6: "SELECT producto.nombre as Producto from producto join departamento on producto.departamento_id=departamento.departamento_id group by departamento.nombre;",
            7: "SELECT producto.nombre as Producto from producto join departamento on producto.departamento_id=departamento.departamento_id WHERE producto.perecedero=true AND departamento.nombre={};".format(raw_input("Introduzca el nombre de departamento a buscar: ")),
            8: "SELECT proveedor.nombre as Proveedor from producto join proveedor on producto.proveedor_id=proveedor.proveedor_id WHERE producto.perecedero=true;",
            9: "SELECT count(*) as Productos, proveedor.nombre as Proveedor from producto join proveedor on producto.proveedor_id=proveedor.proveedor_id group by proveedor.proveedor_id;",
        }
        cur.execute(opcion_dict[opcion])
        system('clear')
        pprint(cur.fetchall())
        conn.commit()
        cur.close()
        conn.close()

if __name__ == '__main__':
    system('clear')
    main()
