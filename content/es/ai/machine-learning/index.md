---
title: Machine Learning
description: El toolkit clásico de ML y el workflow supervisado: los métodos y hábitos que todavía sostienen (y llegan a producción más que) mucha "AI".
tags: [machine-learning, supervised-learning]
order: 0
updated: 2026-06-07
---
# Machine Learning

Donde [[ai/foundations/index|Fundamentos]] contiene los conceptos agnósticos al modelo,
esta rama es el **toolkit clásico práctico**: los algoritmos, el workflow supervisado y
los hábitos que deciden si un modelo es confiable. Mucho de esto precede al deep
learning; y para datos tabulares todavía gana, llega más rápido a producción y es mucho
más fácil de debuggear que una red neuronal.

> Regla práctica: probá un árbol con gradient boosting antes que una red neuronal sobre
> datos tabulares. Empezá simple; ganate la complejidad.

## Modelo mental

Machine learning estadístico selecciona una hipótesis desde datos bajo un loss, regularización y protocolo de validación. Representación, leakage, calibración y análisis de errores deciden si el resultado sobrevive al despliegue.

## Hoja de ruta: workflow y algoritmos

- [[ai/machine-learning/supervised-learning-workflow|El workflow de aprendizaje supervisado, de punta a punta]]
- [[ai/machine-learning/error-analysis|Análisis de errores: leer los errores de tu modelo]]
- [[ai/machine-learning/ml-pipelines-and-leakage|Pipelines y prevención de leakage en preprocesamiento]]

## Algoritmos centrales

- [[ai/machine-learning/linear-and-logistic-regression|Regresión lineal y logística]]
- [[ai/machine-learning/decision-trees-and-ensembles|Árboles de decisión y ensembles (RF, gradient boosting)]]
- [[ai/machine-learning/knn-and-svm|kNN y SVM: distancia y márgenes]]
- [[ai/machine-learning/clustering-and-pca|Clustering y PCA: aprender sin etiquetas]]

## Hacer que los modelos funcionen

- [[ai/machine-learning/feature-engineering|Feature engineering]]
- [[ai/machine-learning/regularization-l1-l2|Regularización: L1, L2 y cómo difieren]]
- [[ai/machine-learning/cross-validation|Cross-validation bien hecha]]
- [[ai/machine-learning/class-imbalance|Manejar class imbalance]]
- [[ai/machine-learning/hyperparameter-tuning|Tuning de hiperparámetros]]

**Conecta con:** [[ai/foundations/index|Fundamentos del Aprendizaje]] · [[ai/data-for-ai/index|Datos para IA]] · [[ai/evaluation/index|Evaluación]]

## Fuentes principales

- James, Witten, Hastie, Tibshirani — *An Introduction to Statistical Learning* (ISLP).
- Aurélien Géron — *Hands-On Machine Learning* (3rd ed.).
- Andrew Ng — *Machine Learning Specialization* (Coursera).
- scikit-learn — *User Guide* (la referencia práctica canónica).
- StatQuest — intuición de árboles, boosting y ROC/PR.
- [An Introduction to Statistical Learning](https://www.statlearning.com/) — teoría y labs reproducibles.
- [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/) — tratamiento avanzado.
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — semántica de implementación.
