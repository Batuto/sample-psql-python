#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
import logging
from pprint import pprint
from os import system
import sys
from terminaltables import AsciiTable
import csv
import time


conn = False
cur = False

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
    cur.execute("CREATE TABLE producto( producto_id int, primary key(producto_id), nombre varchar(50), departamento_id int, descripcion text, perecedero bool, proveedor_id int, precio_compra float, precio_venta float);")
    cur.execute("CREATE TABLE departamento( departamento_id int, primary key(departamento_id), nombre varchar(20));")
    cur.execute("CREATE TABLE proveedor( proveedor_id int, primary key( proveedor_id), nombre varchar(30), telefono char(10));")
    conn.commit()
    sys.exit()

def main():
    global conn, cur
    try:
        conn = connection()
        cur = conn.cursor()
    except:
        logging.warning("Unable to connect")
    while True:
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
            9 - La cantidad de productos que provee un proveedor.

            >>"""
        ))
        opcion_dict = {
                1: lambda: "SELECT producto.nombre AS Nombre, proveedor.nombre AS Proveedor FROM producto JOIN proveedor ON producto.proveedor_id=proveedor.proveedor_id GROUP BY proveedor.nombre, producto.nombre;",
                2: lambda: "SELECT proveedor.nombre AS Proveedor FROM producto JOIN proveedor ON producto.proveedor_id=proveedor.proveedor_id WHERE producto.nombre='%s';" % (raw_input("Introduzca el nombre de producto a buscar: ")),
                3: lambda: "SELECT departamento.nombre as Departamento FROM producto join departamento on producto.departamento_id=departamento.departamento_id WHERE producto.nombre='%s';" % (raw_input("Introduzca el nombre de producto a buscar: ")),
                4: lambda: "SELECT proveedor.nombre as Proveedor from producto join proveedor on producto.proveedor_id=proveedor.proveedor_id join departamento on producto.departamento_id=departamento.departamento_id where departamento.nombre='%s' GROUP BY proveedor.nombre;" % (raw_input("Introduzca el nombre de departamento a buscar: ")),
                5: lambda: "SELECT producto.nombre as Producto from producto join departamento on producto.departamento_id=departamento.departamento_id WHERE departamento.nombre='%s';" % (raw_input("Introduzca el nombre de departamento a buscar: ")),
                6: lambda: "SELECT departamento.nombre, producto.nombre as Producto from producto join departamento on producto.departamento_id=departamento.departamento_id group by departamento.nombre, producto.nombre ORDER BY 1;",
                7: lambda: "SELECT producto.nombre as Producto from producto join departamento on producto.departamento_id=departamento.departamento_id WHERE producto.perecedero=true AND departamento.nombre='%s';" % (raw_input("Introduzca el nombre de departamento a buscar: ")),
                8: lambda: "SELECT proveedor.nombre as Proveedor from producto join proveedor on producto.proveedor_id=proveedor.proveedor_id WHERE producto.perecedero=true GROUP BY proveedor.nombre;",
                9: lambda: "SELECT count(*) as Productos, proveedor.nombre as Proveedor from producto join proveedor on producto.proveedor_id=proveedor.proveedor_id group by proveedor.proveedor_id;",
        }
        cur.execute(opcion_dict[opcion]())
        system('clear')
        output = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        table_data = [colnames,]
        for row in output:
            table_data.append(list(row))
        table = AsciiTable(table_data)
        print table.table
        guardar = raw_input("\n\n\t¿Desea guardar esta consulta?")
        if guardar[:2].upper() in 'SI':
            timestr = time.strftime("%Y%m%d-%H%M%S")
            with open(timestr + '.csv', 'wb') as csvfile:
                file_write = csv.writer(csvfile) # , delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in table_data:
                    file_write.writerow(row)
                csvfile.close()

if __name__ == '__main__':
    system('clear')
    try:
        main()
    except KeyboardInterrupt:
        system('clear')
        cur.close()
        conn.close()
        #logging.basicConfig(format="%(message)s")
        logging.info("Terminating program...")
        print "\n\n\t[x] Terminating program...\n"
        sys.exit()
