#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned int seed = 0x13377331;
int init = 0;

int main() {
  char c;
  char str[] = "1_n3}f3br9Ty{_6_rHnf01fg_14rlbtB60tuarun0c_tr1y3";
  int sLen = strlen(str);
  int n[sLen];
  int rn;
  
  if (init == 0) {
    srand(seed);
    init = 1;
  }

  for (int i = 0; i < sLen; i++) {
    n[i] = rand_r(&seed);
  }

  int i = sLen - 1;
  do {
    rn = n[i];

    c = str[i];
    str[i] = str[rn % (sLen - i) + i];
    str[rn % (sLen -i) + i] = c;

    i = i - 1;
  } while (i >= 0);

  printf("%s\n", str);
  return 0;
}
