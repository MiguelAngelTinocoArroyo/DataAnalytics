import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Reporte de datos de crétido hipotecario')

@st.cache(allow_output_mutation=True)
def load_data(nrows):
    datos = pd.read_csv('./Data/AdquisicionHIP_Train.csv', nrows=nrows)
    return datos

df_load_state = st.text('Cargando data ...')
datos = load_data(8486)

df = pd.read_csv('./Data/AdquisicionHIP_Train.csv')

if st.checkbox('Mostrar datos crudos'):
    st.subheader('Datos crudos')
    st.write(datos)
#-------------------------------------------------------------
# Función para descargar csv
@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

csv = convert_df(df)
st.download_button('Descargar datos crudos',csv,'AdquisicionHIP_Train.csv','text/csv',key='download-csv')
#--------------------------------------------------------------
# Función distancia entre cuartiles:)
def dist_inter_cuartil(df, variable, distancia):
    
    IQR = df[variable].quantile(0.75) - df[variable].quantile(0.25)
    limite_inf = df[variable].quantile(0.25) - (IQR * distancia)
    limite_sup = df[variable].quantile(0.75) + (IQR * distancia)
    
    return limite_sup, limite_inf

# Encontremos los límites superior e inferior para la variable 'EDAD'
EDAD_limite_sup, EDAD_limite_inf = dist_inter_cuartil( df ,'EDAD' , 1.5)
# Encontremos los límites superior e inferior para la variable 'NUMERO_DEPENDIENTES'
NUMERO_DEPENDIENTES_limite_sup,NUMERO_DEPENDIENTES_limite_inf = dist_inter_cuartil(df,'NUMERO_DEPENDIENTES',1.5)
# Encontremos los límites superior e inferior para la variable 'ANTIGUEDAD_DOMICILIO'
ANTIGUEDAD_DOMICILIO_limite_sup,ANTIGUEDAD_DOMICILIO_limite_inf = dist_inter_cuartil(df,'ANTIGUEDAD_DOMICILIO',1.5)
# Encontremos los límites superior e inferior para la variable 'LIQUIDEZDISPONIBLE'
LIQUIDEZDISPONIBLE_limite_sup, LIQUIDEZDISPONIBLE_limite_inf = dist_inter_cuartil(df,'LIQUIDEZDISPONIBLE',1.5)
# Encontremos los límites superior e inferior para la variable 'MARGENOPERATIVO'
MARGENOPERATIVO_limite_sup, MARGENOPERATIVO_limite_inf = dist_inter_cuartil(df,'MARGENOPERATIVO',1.5)

##### Reemplazando los valores:
# Reemplazando los valores extremos de la variabe 'EDAD' 
df['EDAD'] = np.where(df['EDAD'] > EDAD_limite_sup, EDAD_limite_sup,
             np.where(df['EDAD'] < EDAD_limite_inf, EDAD_limite_inf, df['EDAD'])) 

# Reemplazando los valores extremos de la variabe 'NUMERO_DEPENDIENTES'
df['NUMERO_DEPENDIENTES'] = np.where(df['NUMERO_DEPENDIENTES']> NUMERO_DEPENDIENTES_limite_sup,
                            NUMERO_DEPENDIENTES_limite_sup,
                            np.where(df['NUMERO_DEPENDIENTES'] < NUMERO_DEPENDIENTES_limite_inf, 
                            NUMERO_DEPENDIENTES_limite_inf, df['NUMERO_DEPENDIENTES']))

# Reemplazando los valores extremos de la variabe 'ANTIGUEDAD_DOMICILIO'
df['ANTIGUEDAD_DOMICILIO'] = np.where(df['ANTIGUEDAD_DOMICILIO'] >ANTIGUEDAD_DOMICILIO_limite_sup,
                             ANTIGUEDAD_DOMICILIO_limite_sup,
                             np.where(df['ANTIGUEDAD_DOMICILIO'] < ANTIGUEDAD_DOMICILIO_limite_inf, 
                             ANTIGUEDAD_DOMICILIO_limite_inf, df['ANTIGUEDAD_DOMICILIO']))

# Reemplazando los valores extremos de la variabe 'LIQUIDEZDISPONIBLE' 
df['LIQUIDEZDISPONIBLE'] = np.where(df['LIQUIDEZDISPONIBLE'] > LIQUIDEZDISPONIBLE_limite_sup, 
                           LIQUIDEZDISPONIBLE_limite_sup,
                           np.where(df['LIQUIDEZDISPONIBLE'] < LIQUIDEZDISPONIBLE_limite_inf, 
                           LIQUIDEZDISPONIBLE_limite_inf, df['LIQUIDEZDISPONIBLE']))

# Reemplazando los valores extremos de la variabe 'MARGENOPERATIVO'
df['MARGENOPERATIVO'] = np.where(df['MARGENOPERATIVO'] > MARGENOPERATIVO_limite_sup, 
                           MARGENOPERATIVO_limite_sup,
                           np.where(df['MARGENOPERATIVO'] < MARGENOPERATIVO_limite_inf, 
                           MARGENOPERATIVO_limite_inf, df['MARGENOPERATIVO']))
#  1--------------------------------------------------------------------------------------------------

st.subheader('1. Cantidad de personas por Rango de edades:')
import copy
edad = copy.copy(df['EDAD'])

edad_1 = []
edad_2 = [] 
edad_3 = [] 
edad_4 = [] 
edad_5 = []
edad_6 = []

for i in range(0, len(df['EDAD'])) :
    if edad[i] >= 18 and edad[i] <= 30: 
        edad_1.append(edad[i])
    elif edad[i] >= 31 and edad[i] <= 40:
        edad_2.append(edad[i])
    elif edad[i] >= 41 and edad[i] <= 50:
        edad_3.append(edad[i])
    elif edad[i] >= 51 and edad[i] <= 60:
        edad_4.append(edad[i])
    elif edad[i] >= 61 and edad[i] <= 70:
        edad_5.append(edad[i])
    elif edad[i] >= 71 and edad[i] <= 80:
        edad_6.append(edad[i])

eje_x = ['18-30','31-40','41-50','51-60','61-70','71-80']
eje_y = [len(edad_1),len(edad_2),len(edad_3),len(edad_4),len(edad_5),len(edad_6)]
fig1 = px.bar(x = eje_x, y = eje_y, color =['2818','2270','1813','1132','426','27'], text_auto='.2s')
st.plotly_chart(fig1, use_container_width = True)

Rangos = ['18-30','31-40','41-50','51-60','61-70','71-80']
cantidad_personas = ['2818','2270','1813','1132','426','27']

df1 = pd.DataFrame()
df1['Rangos'] = Rangos
df1['cantidad de personas'] = cantidad_personas

st.write(df1)  
#2  -----------------------------------------------------------------------
st.subheader('2. Cantidad de personas por condición de vivienda:')
vivienda_x_edad = df.groupby('CONDICION_VIVIENDA').agg({'EDAD':'count'})['EDAD']
vivienda_x_edad_fig = px.bar(vivienda_x_edad, x=vivienda_x_edad.index, y='EDAD', text_auto='.2s',
                            color=['Alquilado', 'De familiar','Propio'])

st.plotly_chart(vivienda_x_edad_fig , use_container_width = True)
st.write(vivienda_x_edad)

#3-----------------------------------------------------------------------
st.subheader('3. Promedio de edades por condición de vivienda:')
 
C_vivienda = df.groupby(['CONDICION_VIVIENDA']).agg({'EDAD':'mean'})['EDAD']
C_vivienda_fig = px.bar(C_vivienda, x=C_vivienda.index, y='EDAD',
                                                            text_auto='.2s',color=C_vivienda.index)
st.plotly_chart(C_vivienda_fig, use_container_width = True)
st.write(C_vivienda)
# 4------------------------------------------------------------------------
st.subheader('4. Margen operativo por grado de instrucción:')
margen_grado = df.groupby('GRADO_INSTRUCCION').agg({'MARGENOPERATIVO':'count'})['MARGENOPERATIVO']                       
margen_grado_fig = px.bar(margen_grado, x=margen_grado.index, y='MARGENOPERATIVO',
                                                            text_auto='.2s',color=margen_grado.index)
st.plotly_chart(margen_grado_fig, use_container_width = True)
st.write(margen_grado)

# 5------------------------------------------------------------------------
st.subheader('5. Promedio de edades por estado civil:')
prom_civil= df.groupby('ESTADO_CIVIL').agg({'EDAD':'mean'})['EDAD']
prom_civil_fig =px.bar(prom_civil,x=prom_civil.index, y='EDAD',
                                                        text_auto='.2s',color=prom_civil.index)
st.plotly_chart(prom_civil_fig, use_container_width = True)
st.write(prom_civil)


# 6--------------------------------------------------------------
st.subheader('6. Promedio de edades por Genero:')

prom_edad_genero= df.groupby('GENERO').agg({'EDAD':'mean'})['EDAD']
prom_edad_genero_fig =px.bar(prom_edad_genero,x=prom_edad_genero.index, y='EDAD',
                                                        text_auto='.2s',color=prom_edad_genero.index)
st.plotly_chart(prom_edad_genero_fig, use_container_width = True)
st.write(prom_edad_genero)

#-7 ------------------------------------------
st.subheader('7. Cantidad de personas por departamento en el Perú:')
cant_depart = df.groupby('DPTO_DOMICILIO').agg({'EDAD':'count'})['EDAD']
cant_depart_fig = px.bar(cant_depart, x=cant_depart.index, y='EDAD', color=cant_depart.index)
st.plotly_chart(cant_depart_fig, use_container_width = True)
st.write(cant_depart)

# 8---------------------------------------------------------------

st.subheader('8. Cantidad promedio de personas por departamento en el Perú:')
mean_x_depart = df.groupby('DPTO_DOMICILIO').agg({'EDAD':'mean'})['EDAD']
tmean_x_depart_fig = px.bar(mean_x_depart, x=mean_x_depart.index, y='EDAD', color=mean_x_depart.index)
st.plotly_chart(tmean_x_depart_fig, use_container_width = True)
st.write(mean_x_depart)
