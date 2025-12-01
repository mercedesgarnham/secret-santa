import streamlit as st
import pandas as pd
import random

st.title("🎅 Secret Santa")

# Inicializar session_state
if "asignaciones" not in st.session_state:
    st.session_state.asignaciones = None

st.header("1. Cargar nombres")

nombres = st.text_input(
    "Ingresá los nombres separados por coma:",
    placeholder="Ej: Mer, Peter, Vicky, Alan"
)

if st.button("Generar asignaciones"):
    lista = [n.strip() for n in nombres.split(",") if n.strip()]

    if len(lista) < 2:
        st.error("Necesitás al menos 2 personas.")
    else:
        asignados = lista.copy()
        random.shuffle(asignados)

        # Evitar asignación a sí mismo
        while any(a == b for a, b in zip(lista, asignados)):
            random.shuffle(asignados)

        df = pd.DataFrame({"persona": lista, "regala_a": asignados})
        st.session_state.asignaciones = df
        st.success("¡Asignaciones generadas y guardadas de forma oculta!")

# ---------------------------------------------------------------
st.header("2. Consulta tu asignación")

if st.session_state.asignaciones is None:
    st.info("Primero generá las asignaciones arriba.")
else:
    nombre = st.text_input("Ingresá tu nombre para ver a quién le regalás:")

    if st.button("Ver asignación"):
        df = st.session_state.asignaciones

        if nombre not in df["persona"].values:
            st.error("Ese nombre no está en la lista.")
        else:
            destino = df.loc[df["persona"] == nombre, "regala_a"].iloc[0]
            
            # Guardar destino temporalmente para mostrarlo
            st.session_state.mostrar = f"A {nombre} le toca regalarle a: **{destino}**"

    # Mostrar solo si existe
    if "mostrar" in st.session_state:
        st.write(st.session_state.mostrar)

        # Botón para borrar la pantalla
        if st.button("Ocultar"):
            del st.session_state["mostrar"]
            st.rerun()
