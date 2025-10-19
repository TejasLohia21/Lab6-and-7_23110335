#include <stdio.h>

int main() {
    int i = 0;
    int j = 0;
    int k = 0;
    int n = 60;
    int arr[200];
    int aux[200];
    for (i = 0; i < n; i++) {
        arr[i] = (i * i + 3 * i + 7) % 97;
    }
    int sum = 0;
    for (i = 0; i < n; i++) {
        sum = sum + arr[i];
        if (arr[i] % 2 == 0) {
            arr[i] = arr[i] / 2;
        }
        else {
            arr[i] = arr[i] * 3 + 1;
        }
    }
    int even = 0;
    int odd = 0;
    for (i = 0; i < n; i++) {
        if (arr[i] % 2 == 0) {
            even = even + 1;
        }
        else {
            odd = odd + 1;
        }
    }
    int threshold = (sum / n) % 50;
    int greater = 0;
    for (i = 0; i < n; i++) {
        if (arr[i] > threshold) {
            greater = greater + 1;
        }
        else {
            arr[i] = arr[i] + threshold / 2;
        }
    }
    int iteration = 0;
    while (iteration < 100) {
        for (i = 0; i < n; i++) {
            if (arr[i] % 5 == 0) {
                arr[i] = arr[i] + iteration;
            }
            else {
                arr[i] = arr[i] - iteration;
            }
            if (arr[i] < 0) {
                arr[i] = -arr[i];
            }
        }
        iteration = iteration + 1;
    }
    int max = arr[0];
    int min = arr[0];
    for (i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
        if (arr[i] < min) {
            min = arr[i];
        }
    }
    int range = max - min;
    int avg = sum / n;
    int product = 1;
    for (i = 0; i < 15; i++) {
        product = (product * (arr[i] + 1)) % 10000;
    }
    int a = avg;
    int b = range;
    int c = product;
    int d = threshold;
    for (i = 0; i < 120; i++) {
        if (i % 3 == 0) {
            a = (a + b) % 91;
        }
        else if (i % 3 == 1) {
            b = (b + c) % 83;
        }
        else {
            c = (c + d) % 77;
        }
        d = (a + b + c) % 97;
    }
    int final_sum = 0;
    for (i = 0; i < n; i++) {
        final_sum = final_sum + arr[i];
    }
    int pattern = 0;
    for (i = 0; i < n; i++) {
        if (arr[i] % 7 == 0 && arr[i] > avg) {
            pattern = pattern + 1;
        }
        else {
            arr[i] = arr[i] + (avg % 5);
        }
    }
    int x = 0;
    int y = 1;
    int z = 1;
    for (i = 0; i < 60; i++) {
        int temp = (x + y + z) % 200;
        x = y;
        y = z;
        z = temp;
        if (z % 2 == 0) {
            z = z / 2;
        }
        else {
            z = z * 3 + 1;
        }
        if (z > 400) {
            z = z - 300;
        }
    }
    int counter = 0;
    while (counter < 180) {
        if (counter % 4 == 0) {
            x = x + y;
        }
        else if (counter % 4 == 1) {
            y = y + z;
        }
        else {
            z = z + x;
        }
        if (x + y + z > 5000) {
            x = x / 3;
            y = y / 3;
            z = z / 3;
        }
        counter = counter + 1;
    }
    for (i = 0; i < n; i++) {
        aux[i] = arr[i] % 10;
    }
    for (i = 0; i < n; i++) {
        for (j = i + 1; j < n; j++) {
            if (aux[i] > aux[j]) {
                int temp = aux[i];
                aux[i] = aux[j];
                aux[j] = temp;
            }
        }
    }
    int checksum = 0;
    for (i = 0; i < n; i++) {
        if (aux[i] % 2 == 0) {
            checksum = checksum + aux[i];
        }
        else {
            checksum = checksum - aux[i];
        }
        if (checksum < 0) {
            checksum = -checksum;
        }
    }
    int seqA = 1;
    int seqB = 1;
    int seqC = 1;
    for (i = 0; i < 40; i++) {
        seqA = (seqA + seqB) % 100;
        seqB = (seqB + seqC) % 90;
        seqC = (seqA + seqB) % 80;
        if (seqA % 5 == 0) {
            seqA = seqA + 3;
        }
        else {
            seqA = seqA - 2;
        }
        if (seqB > seqC) {
            seqB = seqB - seqC / 2;
        }
        else {
            seqB = seqB + seqA / 3;
        }
    }
    int total = 0;
    for (i = 0; i < 50; i++) {
        int value = (i * seqA + seqB * seqC) % 99;
        if (value % 2 == 0) {
            total = total + value / 2;
        }
        else {
            total = total + value * 3;
        }
    }
    int verify = total % 111;
    int control = 0;
    for (i = 0; i < 30; i++) {
        control = (control + verify + i) % 127;
        if (control % 3 == 0) {
            control = control / 2;
        }
        else {
            control = control + 7;
        }
        if (control > 150) {
            control = control - 120;
        }
    }
    int result = (x + y + z + avg + range + pattern + final_sum + checksum + total + control) % 1000;
    return 0;
}