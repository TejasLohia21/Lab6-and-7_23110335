#include <stdio.h>

int main() {
    int i = 0;
    int j = 0;
    int n = 60;
    int arr[120];
    int aux[120];
    int total = 0;
    int x = 3;
    int y = 7;
    int z = 9;
    int balance = 0;
    int iteration = 0;
    int mode = 1;
    for (i = 0; i < n; i++) {
        arr[i] = (i * 13 + 5 * (i % 7) + 11) % 97;
    }
    for (i = 0; i < n; i++) {
        total = total + arr[i];
        aux[i] = arr[i] % 10;
    }
    int average = total / n;
    int pivot = (average % 20) + 10;
    for (i = 0; i < n; i++) {
        int value = arr[i];
        if (value > pivot) {
            value = value - (value / 5);
            arr[i] = value + (i % 7);
            aux[i] = aux[i] + (arr[i] % 3);
            x = x + 2;
            y = y - 1;
            z = z + (x + y) % 5;
            balance = balance + value - pivot;
            for (j = 0; j < 3; j++) {
                value = (value + j + i) % 91;
                balance = balance + (value % 4);
                if (balance % 7 == 0) {
                    value = value + 2;
                }
                else {
                    value = value - 3;
                }
            }
            arr[i] = value;
        }
        else {
            value = value + (pivot - value) / 2;
            x = x + (value % 3);
            y = y + (x % 4);
            z = z - (y % 5);
            balance = balance - value + pivot;
            for (j = 0; j < 2 * (i % 3 + 1); j++) {
                value = (value + 5 + j) % 97;
                if (value % 6 == 0) {
                    x = x + j;
                }
                else {
                    y = y + i;
                }
                if (x + y + z > 400) {
                    x = x / 2;
                    y = y / 3;
                    z = z / 4;
                }
            }
            arr[i] = value;
            aux[i] = (value + aux[i]) % 11;
        }
    }
    int round = 0;
    while (round < 50) {
        int sumPart = 0;
        for (i = 0; i < n; i++) {
            sumPart = sumPart + arr[i];
        }
        if (sumPart % 2 == 0) {
            for (i = 0; i < n; i++) {
                arr[i] = (arr[i] + i + round) % 100;
                aux[i] = (aux[i] + arr[i]) % 17;
            }
            balance = balance + sumPart / 2;
            x = (x + y + z + balance) % 200;
            y = (y + x / 3 + balance / 4) % 180;
            z = (z + y / 2 + balance / 5) % 160;
        }
        else {
            for (i = n - 1; i >= 0; i--) {
                arr[i] = (arr[i] * 2 + i + round) % 101;
                aux[i] = (aux[i] * 3 + arr[i]) % 19;
            }
            balance = balance - sumPart / 3;
            if (balance < 0) {
                balance = -balance / 2 + 17;
            }
            x = (x + 5 * balance + y) % 210;
            y = (y + 7 * z + x) % 190;
            z = (z + 9 * x + y) % 170;
        }
        round = round + 1;
        if (round % 7 == 0) {
            mode = mode + 1;
            if (mode > 4) {
                mode = 1;
            }
        }
        if (mode == 1) {
            x = (x + 2 * y) % 150;
            y = (y + 3 * z) % 140;
            z = (z + 5 * x) % 130;
        }
        else if (mode == 2) {
            x = (x * 2 + y / 2) % 160;
            y = (y * 3 + z / 3) % 150;
            z = (z * 4 + x / 4) % 140;
        }
        else if (mode == 3) {
            x = (x + y + z) % 180;
            y = (x * 2 - y) % 170;
            z = (z + 3 * y) % 160;
        }
        else {
            x = (x + y / 2) % 155;
            y = (y + z / 2) % 145;
            z = (z + x / 2) % 135;
        }
    }
    int final_value = 0;
    for (i = 0; i < n; i++) {
        final_value = final_value + (arr[i] + aux[i]) % 99;
        if (final_value % 11 == 0) {
            arr[i] = arr[i] + (final_value % 7);
            aux[i] = aux[i] - (final_value % 5);
            if (aux[i] < 0) {
                aux[i] = -aux[i];
            }
        }
        else {
            arr[i] = arr[i] - (final_value % 9);
            aux[i] = aux[i] + (final_value % 6);
        }
    }
    int stability = 0;
    for (i = 0; i < n; i++) {
        stability = stability + (arr[i] * aux[i]) % 123;
        if (stability > 5000) {
            stability = stability / 2;
        }
    }
    int verify = 0;
    for (i = 0; i < 70; i++) {
        verify = (verify + x + y + z + i) % 201;
        if (verify % 3 == 0) {
            verify = verify / 2 + 7;
        }
        
        else {
            verify = verify + 5;
        }
        if (verify > 180) {
            verify = verify - 90;
        }
    }
    int control = 0;
    for (i = 0; i < 50; i++) {
        control = (control + i * x + y - z) % 300;
        if (control % 4 == 0) {
            x = (x + control / 3) % 160;
        } 
        else if (control % 5 == 0) {
            y = (y + control / 2) % 150;
        } 
        else {
            z = (z + control / 4) % 140;
        }
        if (i % 10 == 0) {
            balance = balance + control / 5;
            if (balance % 2 == 0) {
                x = (x + y) % 180;
                y = (y + z) % 170;
            } 
            else {
                x = (x - y) % 190;
                z = (z - x) % 160;
            }
        }
    }
    int cycle = 0;
    while (cycle < 40) {
        if ((x + y + z + balance + cycle) % 9 < 4) {
            x = (x + balance / 2 + cycle) % 210;
            y = (y + x / 3) % 200;
        } 
        else {
            z = (z + balance / 4 + y) % 190;
            balance = (balance + z / 2) % 500;
        }
        cycle++;
    }

    int result = (x + y + z + balance + total + stability + verify + average + pivot + control) % 1000;

    return 0;
}