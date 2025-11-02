from src.etl import run_etl
from src.kpi import run_kpi
from src.model import run_model
from src.evaluation import run_evaluation
from src.dashboards import run_dashboard

def main():
    print("🚀 Iniciando orquestador Fashion Data\n")
    run_etl()
    run_kpi()
    run_model()
    run_evaluation()
    run_dashboard()
    print("\n✅ Pipeline ejecutado con éxito.")

if __name__ == "__main__":
    main()