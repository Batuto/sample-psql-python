#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
import logging
from pprint import pprint
from os import system as sys


def main():
    while True:
        dbname = 'tienda'
        user = raw_input("Introduzca el nombre de usuario: ") 
        pwd = 'password'
        #host = 'localhost'
        host = raw_input("Introduzca el host: ")

        try:
            db_usr = "dbname={0} user={1} host={2} password={3}".format(
                dbname, user, host, pwd)
            conn = psycopg2.connect(db_usr)

        except Exception:
            pprint("Error:")
            logging.basicConfig(format="%(message)s")
            logging.warning("Unable to connect")
            return

        cur = conn.cursor()
        opciones_depa = {
            1: 'lacteos',
            2: 'perfumeria',
            3: 'jardin',
            4: 'abarrotes',
        }
        opciones_ac = {
            1: 'consultar',
            2: 'insertar',
            3: 'modificar',
            4: 'perecedero',
            5: 'descripcion',
            0: 'salir',
        }
        departamento = int(raw_input(
            """Introduzca el número del departamento a acceder:
            1 - Lácteos
            2 - Perfumería
            3 - Jardín
            4 - Abarrotes

    >>"""
            ))
        sys('clear')
        accion = int(raw_input(
            """Introduzca la opción deseada:
            1 - Consultar productos
            2 - Insertar registro
            3 - Modificar nombre de producto
            4 - Mostrar perecederos
            5 - Modificar descripción
            0 - Regresar

    >>"""
            ))
        sys('clear')

        if opciones_ac[accion] == 'consultar':
            try:
                cur.execute("SELECT codigo, nombre,\
                            descripcion FROM productos\
                            WHERE departamento = '{}';".format(
                                opciones_depa[departamento]))
                print "Código\tNombre\t\tDescripción\n"
                for x in cur.fetchall():
                    print x[0],"\t",x[1],"\t\t",x[2]
            except:
                print "Error inesperado\n"

        elif opciones_ac[accion] == 'insertar':
            try:

                nombre = raw_input("Introduce el nombre del producto:\n")
                departamento = raw_input("Introduce el departamento:\n")
                descripcion = raw_input("Introduce la descripción:\n")
                perecedero = 's' in raw_input("Perecedero(s/n)\n").lower()
                proveedor = raw_input("Introduce el proveedor(10 char)\n")[:10]
                cur.execute("INSERT INTO productos(nombre,departamento,descripcion,perecedero,proveedor)\
                            values('{0}','{1}','{2}',{3},'{4}');".format(
                                nombre,departamento,descripcion,perecedero,proveedor))
                conn.commit()
                cur.close()
                conn.close()
            except:
                print "Error inesperado\n"

        elif opciones_ac[accion] == 'modificar':
            codigo = int(
                raw_input('Introduzca el código del producto a modificar:\n'))
            nombre = raw_input(
                "Introduzca el nuevo nombre del producto:\n") or ""
            departamento = raw_input(
                "Introduzca el nuevo nombre de departamento:\n") or ""
            descripcion = raw_input(
                "Introduzca la nueva descripción del producto:\n") or ""

            if nombre:
                nombre = "nombre='{}'".format(nombre)
                cur.execute("UPDATE productos SET {0} WHERE departamento='{1}'\
                            AND codigo={2};".format(
                                nombre, opciones_depa[departamento], codigo))
                conn.commit()
                cur.close()
                conn.close()
        elif opciones_ac[accion] == 'perecedero':
            try:
                cur.execute("SELECT codigo,nombre\
                            FROM productos\
                            WHERE perecedero=True\
                            AND departamento='{0}';".format(
                                opciones_depa[departamento]))
                print "Código\tNombre\n"
                for x in cur.fetchall():
                    print x[0],"\t",x[1]
            except:
                print "Error inesperado\n"
        elif opciones_ac[accion] == 'descripcion':
            codigo = int(
                raw_input('Introduzca el código del producto a modificar:\n'))
            descripcion = raw_input(
                "Introduzca la nueva descripción del producto:\n") or ""
            if descripcion:
                descripcion = "descripcion='{}'".format(descripcion)
                cur.execute(
                    "UPDATE productos SET {0} WHERE codigo={1};".format(
                        descripcion, codigo))
                conn.commit()
                cur.close()
                conn.close()


        elif opciones_ac[accion] == 'salir':
            sys('clear')
            print "\nPrograma terminado.\n"
            cur.close()
            conn.close()
            return

        raw_input("\n\n\n\tPresione enter para continuar...")
        sys('clear')
        continue

if __name__ == '__main__':
    sys('clear')
    main()
