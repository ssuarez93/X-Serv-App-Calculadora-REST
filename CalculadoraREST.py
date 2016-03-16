#!/usr/bin/python
# -*- coding: utf-8 -*-
# Sistemas Teleco. Sara Suárez.

import WebApp
import sys

class CalculadoraREST (WebApp.webApp):

    def parse(self, request):
        """Return the resource name (including /)"""
        metodo = request.split(' ',2)[0]
        try:
            recurso = request.split(' ',2)[1]
        except IndexError:
            return None
        try:
            cuerpo = request.split('\r\n\r\n')[1]
        except IndexError:
            cuerpo =""

        peticion = [metodo, recurso, cuerpo]
        return peticion


    def suma(self, num1, num2):
        return num1 + num2
    def resta(self, num1, num2):
        return num1 - num2
    def multiplicacion(self, num1, num2):
        return num1 * num2
    def division(self, num1, num2):
        try:
            return num1 / num2
        except ZeroDivisionError:
            return None


    def process(self, peticion):

        metodo, recurso, cuerpo = peticion

        if metodo == 'GET':
            try:
                httpCode = "200 OK"
                htmlBody = "La operacion realizada es: " + str(self.operacion) + \
                            "=" + str(self.resultado)
            except AttributeError:
                httpCode = "200 OK"
                htmlBody = "<b>Bienvenido a la aplicacion calculadora. Usa POSTER para hacer PUT y GET</b>"


        elif metodo == 'PUT':
            httpCode = "200 OK"
            htmlBody = "La operacion se ha realizado correctamente. " + \
                        "Para consultarla realiza un GET."
            if len(cuerpo.split(','))==2:
                try:
                    num1 = float(cuerpo.split(',')[0])
                    num2 = float(cuerpo.split(',')[1])
                except TypeError:
                    httpCode = "400 Bad Request"
                    htmlBody = "Solo se admiten operaciones con dos numeros separados por ,"

                if recurso == '/suma':
                    self.operacion = str(num1) + "+" + str(num2)
                    self.resultado = self.suma(num1, num2)
                elif recurso == '/resta':
                    self.operacion = str(num1) + "-" + str(num2)
                    self.resultado = self.resta(num1, num2)
                elif recurso == '/division':
                    self.operacion = str(num1) + "/" + str(num2)
                    self.resultado = self.division(num1, num2)
                elif recurso == '/multiplicacion':
                    self.operacion = str(num1) + "*" + str(num2)
                    self.resultado = self.multiplicacion(num1, num2)
                else:
                    htmlCode = "400 Bad Request"
                    htmlBody = "Solo se admiten las operaciones: \n/suma" + \
                                "\n/resta\n/division\n/multiplicacion"
            else:
                httpCode = "400 Bad Request"
                htmlBody = "Solo se admiten operaciones con dos numeros"

        else:
            httpCode = "450 Method Not Allowed"
            htmlBody = "Solo se admiten operaciones GET y PUT"

        return (httpCode, htmlBody)


if __name__ == "__main__":
    try:
        testWebApp = CalculadoraREST("localhost", 1234)
    except KeyboardInterrupt:
        print "\n Aplicacion cerrada. Hasta la proxima!"
        sys.exit()
