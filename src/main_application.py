import recommender_system
from ontologia import main_ontology
from knowledge_base import main_kb


def first_scene():
    
    print("BOOKONTOLOGY\n")

    while True:
        
        print("Scegli una opzione:\n\n1)Recommender System\n2)Ontology\n3)Knowledge base\n4)Esci.\n")
        
        opzione = input().lower()
        
        if(opzione == "1") or (opzione == "recommender system"):
            recommender_system.output_recommendation()
               
        elif(opzione == "2") or (opzione == "ontology"):
            main_ontology()
        
        elif(opzione == '3') or (opzione == "knowledge base"):
            main_kb()
        
        elif(opzione == "4") or (opzione == "esci"):
            break
                
        else:
            
            print("opzione non valida, riprova.\n")


if __name__ == '__main__':
    first_scene()
