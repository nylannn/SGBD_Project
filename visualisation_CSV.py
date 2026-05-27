################################################################################
# PARTIE 4
################################################################################
import csv

from sqlalchemy import select, func, extract
from base import session

from model_medecin import Medecin
from model_consultation import Consultation
from model_etablissement import Etablissement
from model_rendezvous import RendezVous
from model_patient import Patient


def export_csv(rows, filename, headers):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def run():
    consultations_par_medecin = session.execute(
        select(
            Medecin.id.label("id_medecin"),
            Medecin.nom.label("nom_medecin"),
            Medecin.prenom.label("prenom_medecin"),
            extract("year", Consultation.date_consultation).label("annee"),
            func.count(Consultation.id).label("nb_consultations")
        )
        .join(Consultation, Consultation.id_medecin == Medecin.id)
        .group_by(
            Medecin.id,
            Medecin.nom,
            Medecin.prenom,
            extract("year", Consultation.date_consultation)
        )
        .order_by(Medecin.nom, Medecin.prenom)
    ).all()

    rendezvous_par_etablissement = session.execute(
        select(
            Etablissement.id.label("id_etablissement"),
            Etablissement.nom.label("nom_etablissement"),
            extract("year", RendezVous.date_heure).label("annee"),
            func.count(RendezVous.id).label("nb_rendezvous")
        )
        .join(RendezVous, RendezVous.id_etablissement == Etablissement.id)
        .group_by(
            Etablissement.id,
            Etablissement.nom,
            extract("year", RendezVous.date_heure)
        )
        .order_by(Etablissement.nom)
    ).all()

    consultations_par_patient = session.execute(
        select(
            Patient.id.label("id_patient"),
            Patient.nom.label("nom_patient"),
            Patient.prenom.label("prenom_patient"),
            func.count(Consultation.id).label("nb_consultations")
        )
        .join(Consultation, Consultation.id_patient == Patient.id)
        .where(Consultation.date_consultation >= func.date(func.datetime("now", "-5 years")))
        .group_by(Patient.id, Patient.nom, Patient.prenom)
        .order_by(func.count(Consultation.id).desc())
    ).all()

    export_csv(
        consultations_par_medecin,
        "consultations_par_medecin_et_annee.csv",
        ["id_medecin", "nom_medecin", "prenom_medecin", "annee", "nb_consultations"]
    )

    export_csv(
        rendezvous_par_etablissement,
        "rendezvous_par_etablissement_et_annee.csv",
        ["id_etablissement", "nom_etablissement", "annee", "nb_rendezvous"]
    )

    export_csv(
        consultations_par_patient,
        "consultations_par_patient_5_ans.csv",
        ["id_patient", "nom_patient", "prenom_patient", "nb_consultations"]
    )

    print("[OK] Export CSV terminé.")


if __name__ == "__main__":
    run()