import threading
import time

time_to_delay_max = 2.5
time_to_delay_min = 0.5

# Classe Proposer (Proponente)
class Proposer:
    def __init__(self, proposer_id, acceptors):
        self.proposer_id = proposer_id  # ID do Proponente
        self.acceptors = acceptors  # Lista de Acceptors (Aceitadores)
        self.proposal_number = 0  # Número da proposta inicial

    # Método prepare (preparar)
    def prepare(self):
        self.proposal_number += 1
        print(f"\n\nProponente {self.proposer_id}: Enviando solicitações de preparação com número de proposta {self.proposal_number}\n")
        time.sleep(time_to_delay_max)  # Delay para visualizar solicitações de preparação
        promises = []
        for acceptor in self.acceptors:
            promise = acceptor.receive_prepare(self.proposal_number, self.proposer_id)
            if promise is not None:
                promises.append(promise)
            time.sleep(time_to_delay_max)  # Delay para visualizar a resposta de cada Acceptor

        if len(promises) > len(self.acceptors) // 2:
            highest_proposal = max(promises, key=lambda x: x[0])
            value_to_propose = highest_proposal[1] if highest_proposal[0] != -1 else 1  # Troquei "valor" por 1
            print(f"\n\nProponente {self.proposer_id}: Enviando proposta com o valor {value_to_propose}\n")
            self.propose(value_to_propose)

    # Método propose (propor)
    def propose(self, value):
        time.sleep(time_to_delay_max)  # Delay para visualizar solicitações de proposta
        accepted = []
        for acceptor in self.acceptors:
            ack = acceptor.receive_propose(self.proposal_number, value)
            if ack:
                accepted.append(ack)
            time.sleep(time_to_delay_max)  # Delay para visualizar a resposta de cada Acceptor

        if len(accepted) > len(self.acceptors) // 2:
            print(f"\n\nProponente {self.proposer_id}: Consenso alcançado com valor {value}\n")
            for acceptor in self.acceptors:
                acceptor.learn(value)

# Classe Acceptor (Aceitador)
class Acceptor:
    def __init__(self, acceptor_id):
        self.acceptor_id = acceptor_id  # ID do Aceitador
        self.promised_proposal_number = -1  # Número da proposta prometida
        self.accepted_proposal_number = -1  # Número da proposta aceita
        self.accepted_value = None  # Valor aceito

    # Método receive_prepare (receber preparação)
    def receive_prepare(self, proposal_number, proposer_id):
        print(f"Aceitador {self.acceptor_id + 1}: Recebeu solicitação de preparação com número de proposta {proposal_number} do Proponente {proposer_id}")
        if proposal_number > self.promised_proposal_number:
            self.promised_proposal_number = proposal_number
            time.sleep(time_to_delay_min)
            print(f"Aceitador {self.acceptor_id + 1}: Prometeu aceitar a proposta {proposal_number}")
            return (self.accepted_proposal_number, self.accepted_value)
        time.sleep(time_to_delay_min)
        print(f"Aceitador {self.acceptor_id + 1}: Rejeitando solicitação de preparação com número de proposta {proposal_number}")
        return None

    # Método receive_propose (receber proposta)
    def receive_propose(self, proposal_number, value):
        print(f"Aceitador {self.acceptor_id + 1}: Recebeu solicitação de proposta com o valor {value}")
        if proposal_number >= self.promised_proposal_number:
            self.promised_proposal_number = proposal_number
            self.accepted_proposal_number = proposal_number
            self.accepted_value = value
            time.sleep(time_to_delay_min)
            print(f"Aceitador {self.acceptor_id + 1}: Aceitou a proposta com o valor {value}")
            return True
        time.sleep(time_to_delay_min)
        print(f"Aceitador {self.acceptor_id + 1}: Rejeitando solicitação de proposta com o valor {value}")
        return False

    # Método learn (aprender)
    def learn(self, value):
        time.sleep(time_to_delay_min)
        print(f"Aceitador {self.acceptor_id + 1} aprendeu o valor: {value}")

# Função principal
def main():
    # Criação dos Acceptors (Aceitadores)
    acceptors = [Acceptor(i) for i in range(5)]

    # Criação do Proposer (Proponente)
    proposer = Proposer(proposer_id=1, acceptors=acceptors)

    # Proponente tenta chegar a um consenso
    proposer.prepare()

# Executa a função principal
if __name__ == "__main__":
    main()
