import os
import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk
import re


class Convertor(object):

    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currency = self.data['rates']

    def convert(self, _from, to, amount):
        amount_to_convert = amount

        if _from != 'EUR':
            amount = amount / self.currency[_from]

        amount = round(amount * self.currency[to], 2)  # Limits to 2 decimal places
        return amount


class Display(tk.Tk):

    def __init__(self, convertor):
        tk.Tk.__init__(self)
        self.user_host_name = os.uname()[1]
        self.title = "Currency Convertor"
        self.currency_convertor = convertor

        self.geometry("{}x{}".format(440, 110))
        # self.configure(background='#36393F')

        self.app_label = Label(self, text="Welcome {}!".format(self.user_host_name.upper()), font=('Roboto', 12),
                               fg="cadetblue4", border=2, relief=tk.RAISED)
        self.app_label.grid(row=0, column=0, columnspan=4, pady=10, ipadx=70)

        # Entry box for input and output
        vcmd = (self.register(self.validate_cmd), '%d', '%P')
        self.amount_field = Entry(self, bd=3, font=('Roboto', 12), fg="cadetblue4", relief=tk.RIDGE, justify=tk.CENTER,
                                  validate='key', validatecommand=vcmd)
        self.converted_amount_field_label = Label(self, text='', font=('Roboto', 12), fg="cadetblue4", bg='white',
                                                  relief=tk.RIDGE, justify=tk.CENTER, width=17, borderwidth=3)

        # Dropdown part and default values
        self.currency_from = StringVar(self)
        self.currency_from.set("EUR")

        self.currency_to = StringVar(self)
        self.currency_to.set("TRY")

        self.option_add('*TCombobox*Listbox.font', ('Roboto', 12))
        self.currency_from_dropdown = ttk.Combobox(self, textvariable=self.currency_from,
                                                   values=list(self.currency_convertor.currency.keys()),
                                                   font=('Roboto', 12), state='readonly', width=12, justify=tk.CENTER)

        self.currency_from_dropdown.grid(row=1, column=0)
        self.amount_field.grid(row=2, column=0)

        self.currency_to_dropdown = ttk.Combobox(self, textvariable=self.currency_to,
                                                 values=list(self.currency_convertor.currency.keys()),
                                                 font=('Roboto', 12), state='readonly', width=12, justify=tk.CENTER)

        self.currency_to_dropdown.grid(row=1, column=2)
        self.converted_amount_field_label.grid(row=2, column=2)

        self.convert_btn = Button(self, text='Convert', fg="cadetblue4", font=('Roboto', 12, 'bold'),
                                  command=self.run_convertion)
        self.convert_btn.grid(row=2, column=1)

    def run_convertion(self):
        get_amount = float(self.amount_field.get())
        currency_from = self.currency_from.get()
        currency_to = self.currency_to.get()

        converted_amount = self.currency_convertor.convert(currency_from, currency_to, get_amount)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_field_label.config(text=str(converted_amount))

    def validate_cmd(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))


if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/EUR'
    convert = Convertor(url)
    Display(convert)
    mainloop()
