#include <stdio.h>

int main() {
    int n = 200;
    int data[256];
    int temp[256];
    int aux[256];
    int mirror[256];
    int i = 0, j = 0, k = 0;
    int total = 0;
    int pos = 0, neg = 0, zero = 0;
    int rangeLow = -150;
    int rangeHigh = 150;
    int alpha = 3, beta = 7, gamma = 5;
    int mod = 97;
    int balance = 0;
    int flag = 0;
    int adjust = 0;
    int iteration = 0;
    int offset = 0;
    int shift = 1;
    int rolling = 0;
    int bigSum = 0;
    int result = 0;
    int value = 0;
    int current = 0;
    int next = 0;
    int limit = 180;

    for (i = 0; i < n; i++) {
        data[i] = (i * alpha + i * i * beta + gamma) % mod;
        temp[i] = (data[i] + i * 4) % 89;
        aux[i] = (temp[i] - i * 3 + 17) % 77;
        mirror[i] = (aux[i] + data[i]) % 65;

        if (data[i] > 50) {
            data[i] = data[i] - 30;
        }
        else if (data[i] < -20) {
            data[i] = data[i] + 10;
        }
        else {
            data[i] = data[i] + 5;
        }

        if (data[i] % 2 == 0) {
            pos++;
        }
        else if (data[i] % 3 == 0) {
            neg++;
        }
        else {
            zero++;
        }

        total += data[i];
    }

    for (i = 0; i < n; i++) {
        int t = data[i];
        t = (t * 7 + 13) % 111;

        if (t > 70) {
            t = t - (i % 7);
        }
        else if (t < 20) {
            t = t + (i % 11);
        }
        else {
            t = t * 2 - (i % 9);
        }

        temp[i] = t;
        balance += t % 5;
    }

    for (iteration = 0; iteration < 50; iteration++) {
        for (i = 0; i < n; i++) {
            int m = (data[i] + iteration * 3 + i * 2) % 123;
            if (m < 0) {
                m = -m;
            }

            if (m % 2 == 0) {
                m = m / 2;
            }
            else {
                m = m * 3 + 1;
            }

            data[i] = (data[i] + m - iteration) % 150;
            if (data[i] < 0) {
                data[i] = -data[i];
            }
        }

        if (iteration % 10 == 0) {
            shift++;
        }
        else if (iteration % 7 == 0) {
            shift += 2;
        }
        else {
            shift += 1;
        }

        rolling = (rolling + shift + iteration * 3) % 777;
    }

    for (i = 0; i < n; i++) {
        aux[i] = (data[i] + temp[i] + aux[i] + i * 2) % 201;

        if (aux[i] > 100) {
            aux[i] = aux[i] / 2;
        }
        else if (aux[i] < 30) {
            aux[i] = aux[i] + 15;
        }
        else {
            aux[i] = aux[i] + aux[i] % 9;
        }
    }

    for (i = 0; i < n; i++) {
        int sumBlock = 0;
        for (j = 0; j < 10; j++) {
            int idx = (i + j) % n;
            sumBlock += data[idx];
        }

        if (sumBlock > 400) {
            data[i] = data[i] - (sumBlock % 50);
        }
        else if (sumBlock < 100) {
            data[i] = data[i] + (sumBlock % 20);
        }
        else {
            data[i] = data[i] + (sumBlock % 10);
        }
    }

    for (i = 0; i < n; i++) {
        if (data[i] < rangeLow) {
            data[i] = rangeLow + (i % 5);
        }
        else if (data[i] > rangeHigh) {
            data[i] = rangeHigh - (i % 3);
        }
        else {
            data[i] = data[i] + (i % 2);
        }
    }

    int counter = 0;
    while (counter < 60) {
        for (i = 0; i < n; i++) {
            int t = data[i];

            if (t % 5 == 0) {
                t = t + counter;
            }
            else if (t % 3 == 0) {
                t = t - counter / 2;
            }
            else {
                t = t + counter / 3;
            }

            if (t < 0) {
                t = -t;
            }

            data[i] = t;
        }

        counter++;
    }

    for (i = 0; i < n; i++) {
        if (data[i] % 2 == 0) {
            bigSum += data[i] / 2;
        }
        else if (data[i] % 3 == 0) {
            bigSum += data[i] * 3;
        }
        else {
            bigSum += data[i];
        }

        if (i % 25 == 0) {
            if (bigSum > 7000) {
                bigSum = bigSum / 2;
            }
            else if (bigSum < 3000) {
                bigSum = bigSum * 2;
            }
            else {
                bigSum = bigSum + 200;
            }
        }
    }

    int pass = 0;
    while (pass < 50) {
        for (i = 1; i < n; i++) {
            if (data[i] < data[i - 1]) {
                int tmp = data[i];
                data[i] = data[i - 1];
                data[i - 1] = tmp;
                flag = 1;
            }
        }

        if (flag == 0) {
            pass = 50;
        }
        else {
            flag = 0;
            pass++;
        }
    }

    for (i = 0; i < n; i++) {
        adjust += (data[i] + aux[i] + temp[i]) % 101;

        if (adjust % 11 == 0) {
            adjust = adjust / 2;
        }
        else if (adjust % 7 == 0) {
            adjust = adjust * 3;
        }
        else {
            adjust = adjust + 5;
        }
    }

    for (i = 0; i < n; i++) {
        int val = (data[i] + temp[i] + aux[i]) % 199;

        if (val % 4 == 0) {
            result += val / 2;
        }
        else if (val % 5 == 0) {
            result += val * 2;
        }
        else {
            result += val + 7;
        }

        if (i % 50 == 0) {
            if (result > 9000) {
                result = result / 3;
            }
            else if (result < 2000) {
                result = result * 2;
            }
            else {
                result = result + 111;
            }
        }
    }
    return 0;
}