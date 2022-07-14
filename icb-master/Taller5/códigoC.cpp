using namespace std;

/***************************************************
 *          Introduccion a la Computacion          *
 *                 Taller 5 - C++                  *
 *                                                 *
 *   Para compilar: g++ -std=c++11 -o t5 t5.cpp    *
 *                                                 *
 ***************************************************/

#include <iostream>
#include <random>
#include <chrono>
#include <cassert>
 
/* Tama~nos de las matrices */
#ifndef N
	#define N 100
#endif

float* matrizCeros()
{
	return new float[N * N]();
}

void matrizAleatoria(float *a)
{
	std::uniform_real_distribution<float> dist(0.0, 1.0);
	std::default_random_engine gen;

	for (auto i = 0; i < N; i++) {
		for (auto j = 0; j < N; j++)
			a[i * N + j] = dist(gen);
	}
}

float medirTiempos(void (*fn)(const float*, const float*, float*), const float* a, const float* b, float* res)
{
	auto t0 = std::chrono::system_clock::now();
	fn(a, b, res);
	auto tf = std::chrono::system_clock::now();
	std::chrono::duration<float> total = tf - t0;
	return total.count();
}

void eliminarMatriz(float *a)
{
	delete [] a;
}

void multMatrices(const float* a, const float* b, float *res)
{
int i, j, k;
    for (i = 0; i < N; i++) {
        for(j = 0; j < N; j++) {
            for(k = 0; k < N; k++) {
                
                res[i * N + j] += a[i * N + k] * b[k * N + j];
            }
                    } 
    }
}



void realizarExperimento()
{
	float *A = matrizCeros();
	float *B = matrizCeros();
	float *C = matrizCeros();
	float tiempo;
	matrizAleatoria(A);
	matrizAleatoria(B);

	tiempo = medirTiempos(multMatrices, A, B, C);

	std::cout << "Tiempo total array: " << tiempo << std::endl;

	eliminarMatriz(A);
	eliminarMatriz(B);
	eliminarMatriz(C);
}

int main()
{
	realizarExperimento();

	return 0;
}
