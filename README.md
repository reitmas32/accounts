# API de Administración de Usuarios

## 1) Ejecutar la aplicacion

```shell
uvicorn main:app --reload --port 7899
```


## 2) Generación de Claves RSA con Python

A continuacion se explica cómo generar un par de claves RSA (privada y pública) utilizando la biblioteca cryptography en Python y se proporcionara contexto sobre la importancia y uso de las claves RSA en la seguridad informática, por ultimo se ofrecera un script práctico para su generación.


### 2.1) Contexto y Fundamentos de las Claves RSA

#### 2.1.1) ¿Qué son las Claves RSA?
RSA es un algoritmo de criptografía asimétrica que utiliza un par de claves: una privada y una pública. La clave privada debe ser mantenida en secreto, mientras que la clave pública puede ser compartida. Este algoritmo permite la encriptación de datos, la creación de firmas digitales y más, asegurando la confidencialidad, integridad y autenticidad de la información.


#### 2.1.1) Uso de Claves RSA
Las claves RSA son fundamentales en diversos sistemas de seguridad, incluyendo:

* JWT (JSON Web Tokens): En la autenticación y autorización de usuarios, donde la firma del token se genera usando la clave privada y se verifica con la clave pública correspondiente.
* Comunicaciones Seguras: Como en SSL/TLS para la seguridad en la web, asegurando que la comunicación entre cliente y servidor sea privada y segura.
* Firmas Digitales: Aseguran que un documento o mensaje no ha sido alterado desde su firma, proporcionando no repudio.

#### 2.1.2) Fundamento Teórico y Práctico
RSA se basa en el principio matemático de que, aunque es fácil calcular el producto de dos números primos grandes, es extremadamente difícil hacer la operación inversa: descomponer un número grande en sus factores primos originales. Esta asimetría computacional es lo que hace que RSA sea seguro para la criptografía.

En la práctica, la seguridad de RSA depende del tamaño de la clave. A mayor tamaño de la clave, mayor seguridad, pero también mayor es el costo computacional. Actualmente, se recomienda utilizar claves de al menos 2048 bits para una seguridad adecuada.


### 2.2) Requisitos
Para seguir este tutorial, necesitas tener Python instalado en tu sistema, así como la biblioteca cryptography. Si aún no tienes instalada la biblioteca, puedes añadirla ejecutando el siguiente comando en tu terminal:

```shell
pip install cryptography
```

### 2.3) Generación de Claves

El siguiente script en Python genera un par de claves RSA (una clave privada y su correspondiente clave pública) y las guarda en archivos .pem.

```python
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

with open("private_key.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

public_key = private_key.public_key()

with open("public_key.pem", "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Clave privada y pública RSA generadas y guardadas.")
```

* public_exponent: Este es un número entero que se utiliza en la operación de cifrado y verificación de firma. Un valor común es 65537 por su eficiencia en cálculos y seguridad.

* key_size: Define el tamaño de la clave generada en bits. Un tamaño de 2048 bits se considera seguro para la mayoría de las aplicaciones, aunque se pueden utilizar tamaños mayores (como 3072 o 4096 bits) para una seguridad incrementada.

* backend: Especifica el backend criptográfico que se utilizará para la operación. El valor default_backend() indica que se usará el backend predeterminado proporcionado por la biblioteca.


## Como correr el proyecto en local con DB local

#### Crear local DB
```bash
docker-compose up db -d
cd src
python3 create_local_db.py
```

#### Crear CONTENEDOR DE dOCKER
```bash
docker-compose up app -d
```
