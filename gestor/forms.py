#forms.py
from django import forms
from django.db.models import Q
from tienda.models import Paises
from tienda.models import TipoClientes
from tienda.models import Clientes
from tienda.models import Transportistas
from tienda.models import Pedidos
from tienda.models import Productos
from tienda.models import Pedidos_Lineas
from tienda.models import Monedas
from tienda.models import Facturas
from tienda.models import Facturas_lineas
from tienda.models import Incoterms
from tienda.models import Albaranes
from tienda.models import Albaranes_lineas

# Author: Dario Fervenza
# Copyright: Copyright (c) [2023], Dario Fervenza
# Version: 0.1.0
# Maintainer: Dario Fervenza
# Email: dario.fervenza.garcia@gmail.com
# Status: Development

class FormularioPaises(forms.ModelForm):
    """ Crea form para crear un nuevo pais
    """
    class Meta:
        model=Paises
        fields="__all__"
class FormularioTipoClientes(forms.ModelForm):
    """ Crea form para crear un nuevo tipo de cliente
    Los tipos de clientes deben ser 1, 2 o 3
    """
    class Meta:
        model=TipoClientes
        fields="__all__"
class FormularioClientes(forms.ModelForm):
    """ Crea form para crear un nuevo cliente
    """
    class Meta:
        model=Clientes
        fields="__all__"
class FormularioTransportistas(forms.ModelForm):
    """ Crea form para crear un nuevo transportista
    """
    class Meta:
        model=Transportistas
        fields="__all__"
class FormularioIncoterms(forms.ModelForm):
    """ Crea form para crear un nuevo incoterm
    """
    class Meta:
        model=Incoterms
        fields="__all__"
class FormularioMonedas(forms.ModelForm):
    """ Crea form para crear una nueva moneda
    """
    class Meta:
        model=Monedas
        fields="__all__"
class FormularioProductos(forms.ModelForm):
    """ Crea form para crear un producto
    """
    class Meta:
        model=Productos
        fields="__all__"
class FormularioPedidos(forms.ModelForm):
    """ Crea form para añadir un nuevo pedido
    """
    class Meta:
        model=Pedidos
        fields=["num_pedido","cliente","fecha"]
        widgets={
            "fecha" : forms.DateInput(
                attrs={"type":"date", "format":"%m/%d/%Y"}
                ),
            }
class FormularioCerrarPedidos(forms.Form):
    """ Crea form para cerrar un pedido
    """
    def __init__(self, *args, **kwargs):
        cliente_name=kwargs.pop("cliente_name", None)
        super().__init__(*args, **kwargs)
        if cliente_name == "todos":
            self.fields["pedido"] = forms.ModelChoiceField(
                label="Pedido",
                queryset=Pedidos.objects.filter(cerrado=False),
                to_field_name="num_pedido",
                widget=forms.Select(attrs={'class': 'form-control'})
                )
        else:
            self.fields["pedido"] = forms.ModelChoiceField(
                label="Pedido",
                queryset=Pedidos.objects.filter(
                    Q(cerrado=False) & Q(cliente=cliente_name)
                    ),
                to_field_name="num_pedido",
                widget=forms.Select(attrs={'class': 'form-control'})
                )
    def cerrar_pedido(self):
        numero_de_pedido = self.cleaned_data["pedido"].num_pedido
        Pedidos.objects\
        .filter(num_pedido=numero_de_pedido)\
        .update(cerrado=True)
        Pedidos_Lineas.objects\
        .filter(num_pedido=numero_de_pedido)\
        .update(cerrado=True)
class FormularioReabrirPedidos(forms.Form):
    """ Crea form para abrir un pedido
    """
    def __init__(self, *args, **kwargs):
        cliente_name = kwargs.pop("cliente_name", None)
        super().__init__(*args, **kwargs)
        if cliente_name == "todos":
            self.fields["pedido"] = forms.ModelChoiceField(
                label="Pedido",
                queryset=Pedidos.objects.filter(cerrado=True),
                to_field_name="num_pedido",
                widget=forms.Select(attrs={'class': 'form-control'})
                )
        else:
            self.fields["pedido"] = forms.ModelChoiceField(
                label="Pedido",
                queryset=Pedidos.objects.filter(
                    Q(cerrado=True) & Q(cliente=cliente_name)
                    ),
                to_field_name="num_pedido",
                widget=forms.Select(attrs={'class': 'form-control'})
                )
    def reabrir_pedido(self):
        numero_de_pedido = self.cleaned_data["pedido"].num_pedido
        Pedidos.objects\
        .filter(num_pedido=numero_de_pedido)\
        .update(cerrado=False)
        Pedidos_Lineas.objects\
        .filter(num_pedido=numero_de_pedido)\
        .update(cerrado=False)
class FormularioLineasPedidos(forms.ModelForm):
    """ Crea form para crear lineas de un pedido
    """
    def __init__(self, cliente_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if cliente_name == "todos":
            queryset = Pedidos_Lineas._meta\
                       .get_field('num_pedido')\
                       .remote_field.model.objects\
                       .filter(cerrado=False)
        else:
            queryset = Pedidos_Lineas._meta\
                       .get_field('num_pedido')\
                       .remote_field.model.objects\
                       .filter(Q(cerrado=False) & Q(cliente=cliente_name))
        self.fields['num_pedido'].queryset = queryset
    class Meta:
        model = Pedidos_Lineas
        fields = ["num_pedido", "codigo_articulo", "cantidad"]
        widgets = {
            "num_pedido" : forms.Select(attrs={'class': 'form-control'}),
            "codigo_articulo" : forms.Select(attrs={'class': 'form-control'}),
            'cantidad' : forms.TextInput(attrs={'class': 'form-control'}),
            }
LineasPedidosFormSet = forms.formset_factory(
    FormularioLineasPedidos,
    extra=5
    )
class FormularioEliminarLineasPedidos(forms.Form):
    """ Crea form para eliminar lineas de un pedido
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.fields["identificador"] = \
            forms.IntegerField(label="Identificador",initial=0,min_value=0)
class FormularioFacturas(forms.ModelForm):
    """ Crea form para crear una factura nueva
    """
    class Meta:
        model = Facturas
        fields = [
            "cliente", "num_factura",
            "fecha_factura", "transportista",
            "moneda", "packaging",
            "iva", "dias_transferencia"
            ]
        widgets = {
            "fecha_factura" : forms.DateInput(
                attrs={"type":"date","format":"%m/%d/%Y"}
                ),
            }
class FormularioCerrarFacturas(forms.Form):
    """ Crea form para cerrar una factura
    """
    def __init__(self, *args, **kwargs):
        cliente_name = kwargs.pop('cliente_name', None)
        super().__init__(*args, **kwargs)
        if cliente_name == "todos":
            self.fields["factura"] = forms.ModelChoiceField(
                label="Factura",
                queryset=Facturas.objects.filter(cerrado=False),
                to_field_name="num_factura"
                )
        else:
            queryset = Facturas.objects.filter(
                Q(cerrado=False) & Q(cliente=cliente_name)
                )
            self.fields["factura"] = forms.ModelChoiceField(
                label="Factura",
                queryset=queryset,
                to_field_name="num_factura"
                )
    def cerrar_factura(self):
        numero_de_factura = \
            self.cleaned_data["factura"].num_factura
        Facturas.objects.filter(
            num_factura=numero_de_factura
            ).update(cerrado=True)
class FormularioFacturasLineas(forms.Form):
    """ Crea form para añadir lineas a una factura
    """
    def __init__(self,
                 order_choices,
                 cliente_actual,
                 *args,
                 **kwargs):
        super().__init__( *args, **kwargs)
        queryset = Facturas.objects.filter(
            Q(cliente=cliente_actual) & Q(cerrado=False)
            )
        self.fields["num_factura"] = forms.ModelChoiceField(
            label="Numero de factura: ",
            queryset=queryset
            )
        for order in order_choices:
            identificador_ped = order.identificador
            num_pedido = order.num_pedido
            codigo_articulo = order.codigo_articulo
            cantidad_restante = order.cantidad-order.cantidad_facturada
            if cantidad_restante > 0:
                label = f"Pedido: {num_pedido} - {codigo_articulo} " \
                      + f"(Cant. restante: {cantidad_restante})"
                self.fields[f"Facturado_{identificador_ped}"] = \
                    forms.IntegerField(
                        label=label,
                        initial=0,
                        min_value=0,
                        max_value=cantidad_restante
                        )
class FormularioEliminarLineasFacturadas(forms.Form):
    """ Crea form para eliminar lineas de una factura
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.fields["identificador"] = forms.IntegerField(
            label="Identificador",
            initial=0,
            min_value=0
            )
class FormularioAlbaranes(forms.ModelForm):
    """ Crea form para crear un nuevo albaran
    """
    class Meta:
        model = Albaranes
        fields = [
            "cliente", "num_albaran",
            "fecha_albaran", "transportista",
            "incoterms", "bultos",
            "medidas"
            ]
        widgets = {
            "fecha_albaran":forms.DateInput(
                attrs={"type":"date","format":"%m/%d/%Y"}
                ),
            }
class FormularioCerrarAlbaranes(forms.Form):
    """ Crea form para cerrar un albaran
    """
    def __init__(self, *args, **kwargs):
        cliente_name = kwargs.pop('cliente_name', None)
        super().__init__(*args, **kwargs)
        if cliente_name == "todos":
            self.fields["albaran"] = forms.ModelChoiceField(
                label="Albaran",
                queryset=Albaranes.objects.filter(cerrado=False),
                to_field_name="num_albaran"
                )
        else:
            queryset = Albaranes.objects.filter(
                Q(cerrado=False) & Q(cliente=cliente_name)
                )
            self.fields["albaran"] = forms.ModelChoiceField(
                label="Albaran",
                queryset=queryset,
                to_field_name="num_albaran"
                )
    def cerrar_albaran(self):
        numero_de_albaran = \
            self.cleaned_data["albaran"].num_albaran
        Albaranes.objects\
        .filter(num_albaran=numero_de_albaran)\
        .update(cerrado=True)
class FormularioAlbaranesLineas(forms.Form):
    """ Crea form para crear lineas de
    un albaran
    """
    def __init__(self,
                 order_choices,
                 cliente_actual,
                 *args,
                 **kwargs
                 ):
        super().__init__( *args, **kwargs)
        queryset = Albaranes.objects.filter(
            Q(cliente=cliente_actual) & Q(cerrado=False)
            )
        self.fields["num_albaran"] = forms.ModelChoiceField(
            label="Numero de albaran: ",
            queryset=queryset
            )
        for order in order_choices:
            identificador_ped = order.identificador
            num_pedido = order.num_pedido
            codigo_articulo = order.codigo_articulo
            cantidad_restante = order.cantidad - order.cantidad_servida
            if cantidad_restante > 0:
                label = f"Pedido: {num_pedido} - {codigo_articulo} " \
                      + f"(Cant. restante: {cantidad_restante})"
                self.fields[f"Servido_{identificador_ped}"] = \
                    forms.IntegerField(
                        label=label,
                        initial=0,
                        min_value=0,
                        max_value=cantidad_restante
                        )
class FormularioEliminarLineasServidas(forms.Form):
    """ Crea form para eliminar lineas de un albaran
    """
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.fields["identificador"] = forms.IntegerField(
            label="Identificador",
            initial=0,
            min_value=0
            )
