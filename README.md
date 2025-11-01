# GetDataFromPontosAcumulados
Acessa o site do EducaDF e coleta os relatórios dos dados acumulados de todas as turmas de um determinado colégio
url do site https://educadf.se.df.gov.br/auth
  1) faz o login no modo servidor
  2) Clica em matrícula -> relatórios -> Relatório de Ponto
  3) Na opção --Selcione um tim de relatório -- escolha Relatório total de pontos acumulados
  4) Nos filtros que se seguem
     4.1) Unidade Escolar - Centro Educacional 03 do Guará
     4.2) Tipo de ensino - Ensino Médio
     4.4) série - passar via loop por 1ª série, 2ª série e 3º séire
     4.5) Turma/Agrupamento - passar via loop por todos
     4.6) Bimestre - fixar no 3º bimestre
  5) Clicar em Filtrar
  6) Clicar em Gerar excel
  7) coletar todos em um pasta
