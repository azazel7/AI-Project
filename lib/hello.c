#include <stdio.h>
#include <Python.h>
#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"
#include "numpy/npy_3kcompat.h"

// Module method definitions
static PyObject* hello_world_c(PyObject *self, PyObject *args) {
    printf("Hello, world!\n");
    Py_RETURN_NONE;
}


static PyObject* hello_numpy_c(PyObject *dummy, PyObject *args)
{
    PyObject *arg1=NULL;
    PyObject *arr1=NULL;
    int nd;

    if (!PyArg_ParseTuple(args, "O", &arg1))
        return NULL;

    arr1 = PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_IN_ARRAY);
    /*
     * my code starts here
     */
    nd=PyArray_NDIM(arr1);

    npy_intp *sp=PyArray_SHAPE(arr1);

    printf("array number of dimension: %ld\n", nd);
    printf("array dimentsion: %ld\n",*sp);

    printf("Print array elements:\n");
    
    for (int i=0; i<*sp; i++)
    {
		printf("%lf ",*((npy_double*)PyArray_GETPTR1(arr1,i)));
        /*printf("%lf ",arr1->data[i]);*/
    }

    printf("\n");

    if (arr1 == NULL)
        return NULL;

    nd = PyArray_NDIM(arr1);   //number of dimensions

    Py_DECREF(arr1);

    return PyInt_FromLong(nd);
}

static PyObject* histogram(PyObject *dummy, PyObject *args)
{
	PyObject *arg1=NULL;
	PyObject *arr1=NULL;
	int nd;

	if (!PyArg_ParseTuple(args, "O", &arg1))
		return NULL;

	arr1 = PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_IN_ARRAY);

	nd=PyArray_NDIM(arr1);

	npy_intp *sp=PyArray_SHAPE(arr1);
	int histo[9] = {0};
	int weights[9] = {-10000, -16, -8, -1, 0, 1, 8, 16, 10000};

	double* data = PyArray_DATA(arr1);
	for (int i=0; i<*sp; i++)
	{
		/*printf("%lf ",*((npy_double*)PyArray_GETPTR1(arr1,i)));*/
		/*printf("%d ",*((npy_int*)PyArray_GETPTR1(arr1,i)));*/
		/*printf("%d ",*((npy_int8*)PyArray_GETPTR1(arr1,i)));*/
		/*printf("%d ", );*/
		int val = (int)data[i];
		/*int val = *((npy_int8*)PyArray_GETPTR1(arr1,i));*/
		/*printf("%d ", val);*/
		histo[val] += 1;
	}
	int sum = 0;
	for(int i = 0; i < 9; ++i)
		sum += histo[i] * weights[i];

	if (arr1 == NULL)
		return NULL;

	return PyInt_FromLong(sum);
}

static PyObject* check_pos(PyObject *dummy, PyObject *args)
{
	PyObject *arg_placement_pos=NULL, *arg_no_empty=NULL, *arg_empty=NULL, *arg_recycling_pos=NULL, *arg_board=NULL;
	PyObject *npy_placement_pos=NULL, *npy_no_empty=NULL, *npy_empty=NULL, *npy_recycling_pos=NULL, *npy_board=NULL;
	int width, height;
	int nd;

	if (!PyArg_ParseTuple(args, "OOOOOii", &arg_board, &arg_placement_pos, &arg_no_empty, &arg_empty, &arg_recycling_pos, &width, &height))
		return NULL;

	npy_board = PyArray_FROM_OTF(arg_board, NPY_DOUBLE, NPY_IN_ARRAY);
	npy_placement_pos = PyArray_FROM_OTF(arg_placement_pos, NPY_DOUBLE, NPY_IN_ARRAY);
	npy_no_empty = PyArray_FROM_OTF(arg_no_empty, NPY_DOUBLE, NPY_IN_ARRAY);
	npy_empty = PyArray_FROM_OTF(arg_empty, NPY_DOUBLE, NPY_IN_ARRAY);
	npy_recycling_pos = PyArray_FROM_OTF(arg_recycling_pos, NPY_DOUBLE, NPY_IN_ARRAY);

	double const* board = PyArray_DATA(npy_board);
	double const* placement_pos = PyArray_DATA(npy_placement_pos);
	double const* no_empty = PyArray_DATA(npy_no_empty);
	double const* empty = PyArray_DATA(npy_empty);
	double const* recycling_pos = PyArray_DATA(npy_recycling_pos);

	npy_intp *shape_board = PyArray_SHAPE(npy_board);
	npy_intp *shape_placement_pos = PyArray_SHAPE(npy_placement_pos);
	npy_intp *shape_no_empty = PyArray_SHAPE(npy_no_empty);
	npy_intp *shape_empty = PyArray_SHAPE(npy_empty);
	npy_intp *shape_recycling_pos = PyArray_SHAPE(npy_recycling_pos);

	for(int i = 0; i < shape_placement_pos[0]; ++i){
		int x = (int)placement_pos[i*shape_placement_pos[1]];
		int y = (int)placement_pos[i*shape_placement_pos[1] + 1];
		if(x < 0 || x >= width || y < 0 || y >= height){
			return PyInt_FromLong(0);
		}
		int idx = x*shape_board[1] + y;
		int val = (int)board[idx];
		int in_recycling = 0;
		//Set in_recycling if [x,y] is in recycling_pos
		for(int j = 0; j < shape_recycling_pos[0]; ++j){
			int x_rec = (int)recycling_pos[j*shape_recycling_pos[1]];
			int y_rec = (int)recycling_pos[j*shape_recycling_pos[1] + 1];
			if(x_rec == x && y_rec == y){
				in_recycling = 1;
				break;
			}
		}
		if(val != 0 && !in_recycling){
			return PyInt_FromLong(0);
		}
		//TODO check recycling pos
	}
	for(int i = 0; i < shape_no_empty[0]; ++i){
		int x = (int)no_empty[i*shape_no_empty[1]];
		int y = (int)no_empty[i*shape_no_empty[1] + 1];
		if(x >= 0 && x < width && y >= 0 && y < height){
			int idx = x*shape_board[1] + y;
			int val = (int)board[idx];
			int in_recycling = 0;
			//Set in_recycling if [x,y] is in recycling_pos
			for(int j = 0; j < shape_recycling_pos[0]; ++j){
				int x_rec = (int)recycling_pos[j*shape_recycling_pos[1]];
				int y_rec = (int)recycling_pos[j*shape_recycling_pos[1] + 1];
				if(x_rec == x && y_rec == y){
					in_recycling = 1;
					break;
				}
			}
			if(val == 0 || in_recycling){
				return PyInt_FromLong(0);
			}
		}
	}
	for(int i = 0; i < shape_empty[0]; ++i){
		int x = (int)empty[i*shape_empty[1]];
		int y = (int)empty[i*shape_empty[1] + 1];
		if(x >= 0 && x < width && y >= 0 && y < height){
			int idx = x*shape_board[1] + y;
			int val = (int)board[idx];
			if(val != 0)
				return PyInt_FromLong(0);
		}
	}
	return PyInt_FromLong(1);
}

static PyMethodDef hello_methods[] = {
        {
                "hello_python", hello_world_c, METH_VARARGS,
                "Print 'hello xxx'"
        },
        {
                "hello_numpy", hello_numpy_c, METH_VARARGS,
                "numpy function tester",
        },
        {
                "histogram", histogram, METH_VARARGS,
                "A function to build a quick histogram.",
        },
        {
                "check_pos", check_pos, METH_VARARGS,
                "A quick critical function of the engine.",
        },
        {NULL, NULL, 0, NULL}
};


static struct PyModuleDef hello_definition = {
        PyModuleDef_HEAD_INIT,
        "hello",
        "A Python module that prints 'hello world' from C code.",
        -1,
        hello_methods
};


PyMODINIT_FUNC PyInit_hello(void) {
    Py_Initialize();
    import_array();
    return PyModule_Create(&hello_definition);
}
