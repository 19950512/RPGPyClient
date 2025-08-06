# RPGPyClient

Cliente Python/PyGame para o RPG multiplayer.

Coloque aqui apenas o código do cliente Python. O backend .NET e outros componentes ficam em suas respectivas pastas.
# RPGConsole PyGame Client

Cliente gráfico em Python usando PyGame e gRPC para o RPGConsole.

## Como rodar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Gere os stubs gRPC a partir do `game.proto`:
   ```bash
   python -m grpc_tools.protoc -I../../RPGShared/Protos --python_out=protos --grpc_python_out=protos ../../RPGShared/Protos/game.proto
   ```
   (Certifique-se de que a pasta `protos/` existe dentro de `PyClient`)

3. Execute o cliente:
   ```bash
   python main.py
   ```

## O que está implementado
- Tela de login (email)
- Estrutura pronta para autenticação gRPC
- Pronto para expandir para interface de jogo em tempo real

## Próximos passos
- Implementar tela de senha
- Conectar e autenticar com o servidor gRPC
- Receber e exibir dados do personagem
- Interface de movimentação e combate em tempo real
