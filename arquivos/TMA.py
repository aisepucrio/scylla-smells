def calcular_media(n1, n2, n3, n4):
    return (n1 + n2 + n3 + n4) / 4

# Exemplo de uso:
media = calcular_media(7, 8, 9, 10)
print(media)  # Saída: 8.5


def criar_usuario(nome, idade, email, cidade, telefone):
    return f"Usuário: {nome}, Idade: {idade}, Email: {email}, Cidade: {cidade}, Telefone: {telefone}"

# Exemplo de uso:
usuario = criar_usuario("Ana", 25, "ana@email.com", "São Paulo", "11999999999")
print(usuario)



def calcular_salario(base, bonus, descontos, impostos, horas_extras, beneficios):
    return base + bonus + horas_extras + beneficios - descontos - impostos

# Exemplo de uso:
salario_final = calcular_salario(3000, 500, 200, 300, 150, 400)
print(salario_final)  # Saída: 3550



def informacoes_pessoais(nome, idade, cpf, rg, endereco, cidade, estado, telefone, email, profissao):
    return {"Nome": nome,"Idade": idade,"CPF": cpf,"RG": rg,"Endereço": endereco,"Cidade": cidade,
        "Estado": estado,
        "Telefone": telefone,
        "Email": email,
        "Profissão": profissao
    }

# Exemplo de uso:
pessoa = informacoes_pessoais("Carlos", 30, "123.456.789-00", "12.345.678-9", "Rua A, 123", "Rio de Janeiro", "RJ", "21999999999", "carlos@email.com", "Engenheiro")
print(pessoa)
