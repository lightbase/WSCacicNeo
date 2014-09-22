# # 1. carregar usuário da sessão
# # 2. carregar objeto usuário
# # 3. pegar grupo do usuário

from wscacicneo.model.user import User


def groupfinder(userid, request):
    user_obj = User(
        nome = 'asdasd',
        matricula = 'asdasd',
        email = 'asdsad',
        orgao = 'asdsad',
        telefone = 'sdasd',
        cargo = 'asdasdasd',
        setor = 'asdasd',
        permissao = 'asdasd',
        senha = 'sadasdasd',
        favoritos = ['asdasdasdasd']
    )
    usuario = user_obj.search_user_by_email(userid)
    permissao = usuario.results[0].permissao
    return [permissao]