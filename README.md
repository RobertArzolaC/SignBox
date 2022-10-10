# Proyecto Carga de archivos SignBox

## Primero clonar proyecto
    
```bash
    git clone https://github.com/RobertArzolaC/SignBox.git
```

## Crear entorno virtual de python e instalar dependencias

```bash
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
```

## Crear carpeta files en la raíz del proyecto

```bash
    mkdir files
```

## Crear archivo .env tomar como ejemplo el archivo example.env

```bash
    cp example.env .env
```

## Correr el servidor

```bash
    flask run
```

## El fomulario se encuentra en el [link](http://0.0.0.0:5000/)
