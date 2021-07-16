#include <stdio.h>

int calculate(int start_num, int operation, int end_num) {

    // 模拟计算器计算
    int result;

    printf("%d\n", start_num);
    printf("%d\n", operation);
    printf("%d\n", end_num);
    if (operation == '+') {
        result = start_num + end_num;
    }
    else if (operation == '-') {
        result = start_num - end_num;
    }
    else if (operation == 'x') {
        result = start_num * end_num;
    }
    else if (operation == '/') {
        result = start_num / end_num;
    }
    else {
        result = 0;
    }
}

int main() {
    printf("Hello, World!\n");
    int ret;
    ret = calculate(2, '-', 5);
    printf("result:%d\n", ret);
    return 0;
}
