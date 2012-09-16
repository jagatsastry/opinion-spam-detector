#include<stdlib.h>
int main() {
	a();
}
int a() {

	int * x = malloc(100);
	free(x);
//	x = NULL;
//	if(x)
	free(x);
	return 0;
}
