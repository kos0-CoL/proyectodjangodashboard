from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    """
    Formulario basado en el modelo Producto (ModelForm).
    Genera automáticamente los campos según el modelo.
    """
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'activo']
        
        # Personalización de widgets (cómo se renderiza cada campo en HTML)
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Laptop HP 15"'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción opcional...'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        # Etiquetas personalizadas (opcional, el modelo ya tiene verbose_name)
        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción',
            'precio': 'Precio ($)',
            'stock': 'Stock disponible',
            'activo': '¿Producto activo?',
        }
        
        # Mensajes de ayuda
        help_texts = {
            'precio': 'Usa punto decimal (ej: 299.99). Mínimo 0.01',
            'stock': 'Cantidad en inventario (mínimo 0)',
        }
    
    def clean(self):
        """
        Validación cruzada a nivel de formulario.
        Se ejecuta después de clean_<field>() de cada campo.
        """
        cleaned_data = super().clean()
        precio = cleaned_data.get('precio')
        stock = cleaned_data.get('stock')
        
        # Ejemplo: si hay stock, el precio debe ser > 0 (ya lo valida el modelo,
        # pero aquí mostramos cómo hacer validaciones cruzadas)
        if stock is not None and stock > 0 and precio is not None and precio <= 0:
            self.add_error('precio', 'El precio debe ser mayor a cero si hay stock disponible.')
        
        return cleaned_data


# También podrías crear un formulario manual (sin ModelForm) para entender la diferencia:
class ProductoFormManual(forms.Form):
    """
    Formulario manual (NO basado en modelo) - solo para fines educativos.
    En la práctica real, usa ModelForm arriba.
    """
    nombre = forms.CharField(
        max_length=100,
        label='Nombre del producto',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    descripcion = forms.CharField(
        required=False,
        label='Descripción',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Precio ($)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    stock = forms.IntegerField(
        min_value=0,
        label='Stock',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    activo = forms.BooleanField(
        required=False,
        initial=True,
        label='¿Activo?',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    # Validación personalizada (ejemplo)
    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a cero.")
        return precio