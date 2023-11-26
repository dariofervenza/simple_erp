#models.py
from datetime import datetime
from datetime import timedelta
from django.db import models


# Author: Dario Fervenza
# Copyright: Copyright (c) [2023], Dario Fervenza
# Version: 0.1.0
# Maintainer: Dario Fervenza
# Email: dario.fervenza.garcia@gmail.com
# Status: Development

class Paises(models.Model):
    """ Crea la tabla de paises
    """
    identificador = models.AutoField(primary_key=True)
    pais = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return str(self.pais)
class TipoClientes(models.Model):
    """ Crea la tabla de tipo de cliente
    """

    tipo_cliente = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return str(self.tipo_cliente)
class Transportistas (models.Model):
    """ Crea la tabla de transportistas
    """
    identificador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return str(self.nombre)
class Monedas(models.Model):
    """ Crea la tabla de monedas
    """
    identificador = models.AutoField(primary_key=True)
    moneda = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return str(self.moneda)
class Incoterms(models.Model):
    """ Crea la tabla de incoterms
    """
    identificador = models.AutoField(primary_key=True)
    incoterms = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return str(self.incoterms)
class Clientes(models.Model):
    """ Crea la tabla de clientes
    """
    identificador = models.AutoField(primary_key=True)
    cliente = models.CharField(max_length=100, unique=True)
    pais = \
        models.ForeignKey(Paises,on_delete=models.CASCADE, to_field="pais")
    tipo_cliente = models.ForeignKey(TipoClientes, on_delete=models.CASCADE)
    direccion_calle_numero = \
        models.CharField(max_length=100,null=True, blank=True)
    direccion_piso = models.CharField(max_length=30, null=True, blank=True)
    direccion_localidad = \
        models.CharField(max_length=40, null=True, blank=True)
    direccion_cp = models.CharField(max_length=20, null=True, blank=True)
    cif_vat = models.CharField(max_length=30, null=True, blank=True)
    fecha_creacion = \
        models.DateTimeField(auto_now_add=True, null=True, blank=True)
    otros_datos1 = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.cliente)
class Productos(models.Model):
    """ Crea la tabla de productos de la tienda
    """
    identificador = models.AutoField(primary_key=True)
    codigo_articulo = models.CharField(max_length=25, unique=True)
    descripcion = models.CharField(max_length=150, unique=True)
    precioTipo1 = models.DecimalField(max_digits=10, decimal_places=3)
    precioTipo2 = models.DecimalField(max_digits=10, decimal_places=3)
    precioTipo3 = models.DecimalField(max_digits=10, decimal_places=3)
    peso_neto = \
        models.DecimalField(max_digits=10, decimal_places=4, default=0)
    def __str__(self):
        return str(self.codigo_articulo)
class Pedidos(models.Model):
    """ Crea la tabla de pedidos
    """
    identificador = models.AutoField(primary_key=True)
    num_pedido = models.IntegerField(unique=True)
    cliente = models.ForeignKey(
        Clientes,on_delete=models.CASCADE,
        to_field="cliente",
        related_name='pedido_cliente_reverse'
        )
    #esto lo useremos luego para, al añadir las lineas de
    #pedidos, desde el modelo de lineas acceder
    #a pedido y añadir el precio total
    id_cliente = models.IntegerField(null=True, blank=True)
    tipo_cliente = \
        models.CharField(max_length=50, blank=True,default="")
    fecha = models.DateField(auto_now_add=False)
    precio_total = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
        )
    cerrado = models.BooleanField(default=False)
    def __str__(self):
        return str(self.num_pedido)
    def save(self, *args,**kwargs):
        self.tipo_cliente = self.cliente.tipo_cliente
        self.id_cliente = self.cliente.identificador
        super().save(*args,**kwargs)
class Pedidos_Lineas(models.Model):
    """ Crea la tabla de lineas de cada pedido
    """
    identificador = models.AutoField(primary_key=True)
    num_pedido = models.ForeignKey(
        Pedidos,
        on_delete=models.CASCADE,
        to_field="num_pedido",
        null=False,
        blank=False
        )
    codigo_articulo=models.ForeignKey(
        Productos,
        on_delete=models.CASCADE,
        to_field="codigo_articulo",
        null=False,
        blank=False
        )
    fecha = models.DateField(null=True, blank=True)
    cliente = models.CharField(max_length=100,default="", blank=True)
    tipo_cliente = \
        models.CharField(max_length=50,default="", blank=True)
    cantidad = models.IntegerField(null=False,blank=False)
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
        )
    precio_total_linea = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
        )
    precio_total_pedido = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
        )
    cantidad_servida = \
        models.IntegerField(null=False,blank=False,default=0)
    cantidad_facturada = \
        models.IntegerField(null=False,blank=False,default=0)
    cerrado = models.BooleanField(default=False)
    def __str__(self):
        response = str(self.num_pedido) \
                 + "-" \
                 + str(self.codigo_articulo)
        return response
    def save(self, *args, **kwargs):
        self.fecha = self.num_pedido.fecha
        self.cliente = self.num_pedido.cliente
        self.tipo_cliente = self.num_pedido.tipo_cliente
        if self.tipo_cliente == "1":
            self.precio_unitario = self.codigo_articulo.precioTipo1
        elif self.tipo_cliente == "2":
            self.precio_unitario = self.codigo_articulo.precioTipo2
        elif self.tipo_cliente == "3":
            self.precio_unitario = self.codigo_articulo.precioTipo3
        self.precio_total_linea = self.cantidad*self.precio_unitario
        super().save(*args, **kwargs)
        precio_total = Pedidos_Lineas.objects\
                      .filter(num_pedido=self.num_pedido)\
                      .aggregate(
                        models.Sum("precio_total_linea")
                        )["precio_total_linea__sum"]
        Pedidos_Lineas.objects\
        .filter(num_pedido=self.num_pedido)\
        .update(precio_total_pedido=precio_total)
        Pedidos.objects\
        .filter(num_pedido=int(str(self.num_pedido)))\
        .update(precio_total=precio_total)
    def delete(self, *args, **kwargs):
        numero_pedido_eliminar = self.num_pedido_id
        super().delete(*args, **kwargs)
        precio_total = Pedidos_Lineas.objects\
                      .filter(num_pedido=numero_pedido_eliminar)\
                      .aggregate(
                        models.Sum("precio_total_linea")
                        )["precio_total_linea__sum"]
        Pedidos_Lineas.objects\
        .filter(num_pedido=self.num_pedido)\
        .update(precio_total_pedido=precio_total)
        Pedidos.objects\
        .filter(num_pedido=int(str(self.num_pedido)))\
        .update(precio_total=precio_total)
class Facturas (models.Model):
    """ Crea la tabla de facturas
    """
    identificador = models.AutoField(primary_key=True)
    num_factura = models.IntegerField(unique=True)
    fecha_factura = \
        models.DateField(auto_now_add=False,blank=False)
    num_pedidos_incluidos = models.CharField(
        max_length=70,
        unique=False,
        blank=False,
        default=""
        )
    transportista = models.ForeignKey(
        Transportistas,
        on_delete=models.CASCADE,
        to_field="nombre",
        blank=False,
        null=False)
    moneda = models.ForeignKey(
        Monedas,
        on_delete=models.CASCADE,
        to_field="moneda",
        blank=False,
        null=False
        )
    cliente = models.ForeignKey(
        Clientes,
        on_delete=models.CASCADE,
        to_field="cliente",
        blank=False,
        null=False
        )
    direccion_calle_numero = models.CharField(
        max_length=100,
        null=True,
        blank=True
        )
    direccion_piso = models.CharField(
        max_length=30,
        null=True,
        blank=True
        )
    direccion_localidad = models.CharField(
        max_length=40,
        null=True,
        blank=True
        )
    direccion_cp = models.CharField(
        max_length=20,
        null=True,
        blank=True
        )
    cif_vat = models.CharField(max_length=30,null=True, blank=True)
    pais = models.CharField(
        max_length=100,
        unique=False,
        null=True,
        blank=True
        )
    packaging = models.CharField(max_length=60,null=True, blank=True)
    iva = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=False,
        blank=False
        )
    dias_transferencia = models.IntegerField(null=False, blank=False)
    fecha_limite_transferencia = models.DateField(
        auto_now_add=False,
        blank=True,
        null=True
        )
    id_cliente = models.IntegerField(blank=True,null=True)
    cerrado = models.BooleanField(default=False)
    def __str__(self):
        return str(self.num_factura)
    def save(self,*args,**kwargs):
        today = datetime.now().date()
        limite = today + timedelta(days=self.dias_transferencia)
        self.fecha_limite_transferencia = limite
        self.id_cliente = self.cliente.identificador
        super().save(*args,**kwargs)
class Facturas_lineas(models.Model):
    """ Crea la tabla de lineas de facturas
    """
    identificador = models.AutoField(primary_key=True)
    identificador_linea_pedido = models.IntegerField(
        blank=True,
        null=True
        )
    num_factura = models.ForeignKey(
        Facturas,
        on_delete=models.CASCADE,
        to_field="num_factura",
        blank=True,
        null=True
        )
    num_pedido = models.ForeignKey(
        Pedidos,
        on_delete=models.CASCADE,
        to_field="num_pedido",
        blank=False,
        null=False
        )
    codigo_articulo = \
        models.CharField(max_length=25, unique=False)
    cantidad_total = \
        models.IntegerField(null=False, blank=False)
    cantidad_facturada = \
        models.IntegerField(null=False,blank=False)
    precio_unitario_linea_pedido = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
        )
    cliente = \
        models.CharField(max_length=100, default="", blank=True)
    def __str__(self):
        return str(self.num_factura)
    def save (self, *args, **kwargs):
        pedido_modificado = Pedidos_Lineas.objects.filter(
            identificador=self.identificador_linea_pedido
            )
        cantidad_facturada_ahora = self.cantidad_facturada
        cantidad_facturada_previa = \
            pedido_modificado.values("cantidad_facturada")\
            .first()["cantidad_facturada"]
        cliente = pedido_modificado\
                  .values("cliente")\
                  .first()["cliente"]
        cliente_objet = \
            Clientes.objects.filter(cliente=cliente)
        direccion_calle_numero = \
            cliente_objet\
            .values("direccion_calle_numero")\
            .first()["direccion_calle_numero"]
        direccion_piso = \
            cliente_objet\
            .values("direccion_piso")\
            .first()["direccion_piso"]
        direccion_localidad = \
            cliente_objet\
            .values("direccion_localidad")\
            .first()["direccion_localidad"]
        direccion_cp = \
            cliente_objet\
            .values("direccion_cp")\
            .first()["direccion_cp"]
        cif_vat = \
            cliente_objet.values("cif_vat").first()["cif_vat"]
        pais = cliente_objet.values("pais").first()["pais"]
        factura = self.num_factura_id
        self.cliente = self.num_factura.cliente
        self.precio_unitario_linea_pedido = \
            pedido_modificado\
            .values("precio_unitario")\
            .first()["precio_unitario"]
        super().save(*args, **kwargs)
        Facturas.objects\
        .filter(num_factura=factura).update(pais=pais)
        Facturas.objects\
        .filter(num_factura=factura)\
        .update(direccion_calle_numero=direccion_calle_numero)
        Facturas.objects\
        .filter(num_factura=factura)\
        .update(direccion_piso=direccion_piso)
        Facturas.objects\
        .filter(num_factura=factura)\
        .update(direccion_localidad=direccion_localidad)
        Facturas.objects\
        .filter(num_factura=factura)\
        .update(direccion_cp=direccion_cp)
        Facturas.objects\
        .filter(num_factura=factura)\
        .update(cif_vat=cif_vat)
        total = cantidad_facturada_previa \
              + cantidad_facturada_ahora
        pedido_modificado.update(cantidad_facturada=total)
        lineas_factura_set = Facturas_lineas.objects\
        .filter(num_factura=factura)
        lista_pedidos = \
            [obj.num_pedido.num_pedido for obj in lineas_factura_set]
        lista_pedidos = set(lista_pedidos)
        lista_pedidos = sorted(lista_pedidos)
        pedido_incluidos = ""
        for el in lista_pedidos:
            pedido_incluidos += str(el) + "/"
        Facturas.objects\
        .filter(num_factura=factura)\
        .update(num_pedidos_incluidos=pedido_incluidos)
    def delete(self, *args, **kwargs):
        identificador_linea_pedido = self.identificador_linea_pedido
        cantidad_eliminada = self.cantidad_facturada
        super().delete(*args, **kwargs)
        cantidad_facturada_previa = \
            Pedidos_Lineas.objects.filter(
                identificador=identificador_linea_pedido
                ).values("cantidad_facturada").first()["cantidad_facturada"]
        cant = cantidad_facturada_previa - cantidad_eliminada
        Pedidos_Lineas.objects\
        .filter(identificador=identificador_linea_pedido)\
        .update(cantidad_facturada=cant)
class Albaranes(models.Model):
    """ Crea la tabla de albaranes
    """
    identificador = models.AutoField(primary_key=True)
    num_albaran = models.IntegerField(unique=True)
    fecha_albaran = models.DateField(auto_now_add=False, blank=False)
    num_pedidos_incluidos = models.CharField(
        max_length=70,
        unique=False,
        blank=False,
        default=""
        )
    transportista = models.ForeignKey(
        Transportistas,
        on_delete=models.CASCADE,
        to_field="nombre",
        blank=False,
        null=False
        )
    incoterms = models.ForeignKey(
        Incoterms,
        on_delete=models.CASCADE,
        to_field="incoterms",
        blank=False,
        null=False
        )
    cliente = models.ForeignKey(
        Clientes,
        on_delete=models.CASCADE,
        to_field="cliente",
        blank=False,
        null=False
        )
    direccion_calle_numero = models.CharField(
        max_length=100,
        null=True,
        blank=True
        )
    direccion_piso = models.CharField(
        max_length=30,
        null=True,
        blank=True
        )
    direccion_localidad = models.CharField(
        max_length=40,
        null=True,
        blank=True
        )
    direccion_cp = models.CharField(
        max_length=20,
        null=True,
        blank=True
        )
    cif_vat = models.CharField(
        max_length=30,
        null=True,
        blank=True
        )
    pais = models.CharField(
        max_length=100,
        unique=False,
        null=True,
        blank=True
        )
    bultos = models.IntegerField(
        null=False,
        blank=False
        )
    medidas = models.CharField(
        max_length=100,
        unique=False,
        null=False,
        blank=True
        )
    id_cliente = models.IntegerField(blank=True, null=True)
    cerrado = models.BooleanField(default=False)
    def __str__(self):
        return str(self.num_albaran)
    def save(self, *args, **kwargs):
        self.id_cliente = self.cliente.identificador
        super().save(*args, **kwargs)
class Albaranes_lineas(models.Model):
    """ Crea la tabla de lineas de albaranes
    """
    identificador = models.AutoField(primary_key=True)
    identificador_linea_pedido = \
        models.IntegerField(blank=True, null=True)
    num_albaran=models.ForeignKey(
        Albaranes,
        on_delete=models.CASCADE,
        to_field="num_albaran",
        blank=True,
        null=True
        )
    num_pedido = models.ForeignKey(
        Pedidos,
        on_delete=models.CASCADE,
        to_field="num_pedido",
        blank=False,
        null=False
        )
    codigo_articulo = models.CharField(
        max_length=25,
        unique=False
        )
    cantidad_total = models.IntegerField(
        null=False,
        blank=False
        )
    cantidad_servida = models.IntegerField(
        null=False,
        blank=False
        )
    cliente = models.CharField(
        max_length=100,
        default="",
        blank=True
        )
    peso_neto = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=0
        )
    def __str__(self):
        return str(self.num_albaran)
    def save (self, *args, **kwargs):
        pedido_modificado = \
            Pedidos_Lineas.objects\
            .filter(identificador=self.identificador_linea_pedido)
        cantidad_servida_ahora = self.cantidad_servida
        cantidad_servida_previa = \
            pedido_modificado\
            .values("cantidad_servida")\
            .first()["cantidad_servida"]
        cliente = \
            pedido_modificado.values("cliente").first()["cliente"]
        cliente_objet = \
            Clientes.objects.filter(cliente=cliente)
        direccion_calle_numero = \
            cliente_objet\
            .values("direccion_calle_numero")\
            .first()["direccion_calle_numero"]
        direccion_piso = \
            cliente_objet\
            .values("direccion_piso")\
            .first()["direccion_piso"]
        direccion_localidad = \
            cliente_objet\
            .values("direccion_localidad")\
            .first()["direccion_localidad"]
        direccion_cp = \
            cliente_objet\
            .values("direccion_cp")\
            .first()["direccion_cp"]
        cif_vat = cliente_objet.values("cif_vat").first()["cif_vat"]
        pais = cliente_objet.values("pais").first()["pais"]
        albaran = self.num_albaran_id
        self.cliente = self.num_albaran.cliente
        self.precio_unitario_linea_pedido = \
            pedido_modificado\
            .values("precio_unitario")\
            .first()["precio_unitario"]
        self.peso_neto = \
            Productos.objects\
            .filter(codigo_articulo=self.codigo_articulo)\
            .values("peso_neto").first()["peso_neto"]
        super().save(*args, **kwargs)
        Albaranes.objects\
        .filter(num_albaran=albaran)\
        .update(pais=pais)
        Albaranes.objects\
        .filter(num_albaran=albaran)\
        .update(direccion_calle_numero=direccion_calle_numero)
        Albaranes.objects\
        .filter(num_albaran=albaran)\
        .update(direccion_piso=direccion_piso)
        Albaranes.objects\
        .filter(num_albaran=albaran)\
        .update(direccion_localidad=direccion_localidad)
        Albaranes.objects\
        .filter(num_albaran=albaran)\
        .update(direccion_cp=direccion_cp)
        Albaranes.objects\
        .filter(num_albaran=albaran)\
        .update(cif_vat=cif_vat)
        total = cantidad_servida_previa + cantidad_servida_ahora
        pedido_modificado\
        .update(cantidad_servida=total)
        lineas_albaran_set = \
            Albaranes_lineas.objects.filter(num_albaran=albaran)
        lista_pedidos = \
            [obj.num_pedido.num_pedido for obj in lineas_albaran_set]
        lista_pedidos = set(lista_pedidos)
        lista_pedidos = sorted(lista_pedidos)
        pedido_incluidos = ""
        for el in lista_pedidos:
            pedido_incluidos += str(el) + "/"
        Albaranes.objects\
        .filter(num_albaran=albaran)\
        .update(num_pedidos_incluidos=pedido_incluidos)
    def delete(self, *args, **kwargs):
        identificador_linea_pedido = self.identificador_linea_pedido
        cantidad_eliminada = self.cantidad_servida
        super().delete(*args, **kwargs)
        cantidad_servida_previa = \
            Pedidos_Lineas.objects\
            .filter(identificador=identificador_linea_pedido)\
            .values("cantidad_servida")\
            .first()["cantidad_servida"]
        total = cantidad_servida_previa-cantidad_eliminada
        Pedidos_Lineas.objects\
        .filter(identificador=identificador_linea_pedido)\
        .update(cantidad_servida=total)
