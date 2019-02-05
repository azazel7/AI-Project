#include <stdio.h>
#include <Python.h>
#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"
#include "numpy/npy_3kcompat.h"

// Module method definitions
static PyObject* hello_world_c(PyObject *self, PyObject *args) {
    /*printf("Hello, world!\n");*/
	int valuable_space[1024];
	for(int i = 0; i < 1024; ++i)
			valuable_space[i] = 0;
    Py_RETURN_NONE;
}

int matching_cells[2][4][4];

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
		int val = (int)data[i];
		histo[val] += 1;
	}
	int sum = 0;
	for(int i = 0; i < 9; ++i)
		sum += histo[i] * weights[i];

	if (arr1 == NULL)
		return NULL;

    Py_DECREF(arr1);
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

	int return_value = 1;
	for(int i = 0; i < shape_placement_pos[0] && return_value == 1; ++i){
		int x = (int)placement_pos[i*shape_placement_pos[1]];
		int y = (int)placement_pos[i*shape_placement_pos[1] + 1];
		if(x < 0 || x >= width || y < 0 || y >= height){
			return_value = 0;
			break;
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
			return_value = 0;
			break;
		}
		//TODO check recycling pos
	}
	for(int i = 0; i < shape_no_empty[0] && return_value == 1; ++i){
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
				return_value = 0;
				break;
			}
		}
	}
	for(int i = 0; i < shape_empty[0] && return_value == 1; ++i){
		int x = (int)empty[i*shape_empty[1]];
		int y = (int)empty[i*shape_empty[1] + 1];
		if(x >= 0 && x < width && y >= 0 && y < height){
			int idx = x*shape_board[1] + y;
			int val = (int)board[idx];
			if(val != 0){
				return_value = 0;
				break;
			}
		}
	}
    Py_DECREF(npy_board);
    Py_DECREF(npy_placement_pos);
    Py_DECREF(npy_no_empty);
    Py_DECREF(npy_empty);
    Py_DECREF(npy_recycling_pos);
	return PyInt_FromLong(return_value);
}

static void count_line(int const x_start,
					   int const y_start,
 					   int const x_offset_mul,
					   int const y_offset_mul,
					   double const* board,
					   npy_intp const* shape_board,
					   int align[2][4],
					   int valuable_space[2][96])
{
	int offset = 0;

	int prev_val = -1;
	int prev_space = -1;
	int count[2];
	do{	
		int x = x_start + offset*x_offset_mul;
		int y = y_start + offset*y_offset_mul;
		if(x < 0 || x >= shape_board[0] || y < 0 || y >= shape_board[1]){
			break;
		}
		int idx = x*shape_board[1] + y;
		int val = board[idx];
		/*First turn, we need to initialize count*/
		if(prev_val == -1){
			if(val != 0)
				count[0] = count[1] = 1;
			else{
				count[0] = count[1] = 0;
				prev_space = idx;
			}
		}
		else{
			if(val == 0){
				if(prev_val > 0){ //The previous value wasn't empty, so we need to count a line of size count[i]
					for(int i = 0; i < 2; ++i){
						if(count[i] > 0){
							align[i][count[i]-1] += 1;
							valuable_space[i][idx] = valuable_space[i][idx] < count[i] ? count[i] : valuable_space[i][idx];
							if(prev_space >= 0){
								valuable_space[i][prev_space] = valuable_space[i][prev_space] < count[i] ? count[i] : valuable_space[i][prev_space];
							}
						}
					}
				}
				count[0] = count[1] = 0;
				prev_space = idx;
			}
			else if(prev_val == 0){
				count[0] = count[1] = 1;
			}
			else{
				/*For both color and dot, check if the previous value match the current value so the serie keep going.*/
				/*For instance, if prev_val and val indicate the same color or the same type of dot.*/
				for(int i = 0; i < 2; ++i){
					if (matching_cells[i][prev_val-1][val-1])
						count[i] += 1;
					else
						count[i] = 1;
					if(count[i] == 4){ //TODO The win_length, but I don't have it here
						align[i][3] += 1;
					}
				}
			}
		}
		prev_val = val;
		offset +=1;
	}while(1);
	if(prev_val > 0){ //The previous value wasn't empty, so we need to count a line of size count[i]
		for(int i = 0; i < 2; ++i){
			if(count[i] > 0){
				align[i][count[i]-1] += 1;
				if(prev_space >= 0){
					valuable_space[i][prev_space] = valuable_space[i][prev_space] < count[i] ? count[i] : valuable_space[i][prev_space];
				}
			}
		}
	}
}
static PyObject* heuristic(PyObject *dummy, PyObject *args)
{
	PyObject *arg_board=NULL;
	PyObject *npy_board=NULL;

	if (!PyArg_ParseTuple(args, "O", &arg_board))
		return NULL;

	npy_board = PyArray_FROM_OTF(arg_board, NPY_DOUBLE, NPY_IN_ARRAY);

	double const* board = PyArray_DATA(npy_board);

	npy_intp *shape_board = PyArray_SHAPE(npy_board);

	int valuable_space[2][shape_board[0] * shape_board[1]];
	for(int i = 0; i < 2; ++i)
		for(int j = 0; j < shape_board[0] * shape_board[1]; ++j)
			valuable_space[i][j] = 0;
	
	int align[2][4]; //Contains the distribution of alignment length
	for(int i = 0; i < 2; ++i)
		for(int j = 0; j < 4; ++j)
			align[i][j] = 0;

	for(int col = 0; col < shape_board[0]; ++col){
		//Check column from (col, 0)
		count_line(col, 0, 0, 1, board, shape_board, align, valuable_space);
		//Check diagonal from (col, 0)
		count_line(col, 0, 1, 1, board, shape_board, align, valuable_space);
		//Check cdiagonal from (col, 0)
		count_line(col, 0, -1, 1, board, shape_board, align, valuable_space);
	}
	for(int row = 0; row < shape_board[1]; ++row){
		//Check row from (0, row)
		count_line(0, row, 1, 0, board, shape_board, align, valuable_space);
		if(row > 0){
			//Check diagonal from (0, row)
			count_line(0, row, 1, 1, board, shape_board, align, valuable_space);
			//Check cdiagonal from (shape_board[0]-1, row)
			count_line(0, row, 1, 1, board, shape_board, align, valuable_space);
		}
	}

	int valuable_space_count[2][4] = {0};
	for(int i = 0; i < 2; ++i)
		for(int j = 0; j < 4; ++j)
			valuable_space_count[i][j]=0;

	for(int i = 0; i < 2; ++i)
		for(int y = shape_board[1]-1; y >= 0; --y)
			for(int x = 0; x < shape_board[0]; ++x){
				int val = valuable_space[i][x*shape_board[1]+y];
				if(val > 0)
					valuable_space_count[i][val- 1] += 1;
			}
	int weight_align[4] = {0, 1, 8, 1000000};
	int weight_vspace[4] = {0, 1, 8, 100000};
//2 vspace à 3 == victoire
//

	int values[2] = {0};
	for(int i = 0; i < 2; ++i){
		/*printf("Align (%d): ", i);*/
		for(int x = 0; x < 4; ++x){
			values[i] += weight_align[x] * align[i][x];
			/*printf("%d ", align[i][x]);*/
		}
		/*printf("\nv space (%d): ", i);*/
		for(int x = 0; x < 4; ++x){
			values[i] += weight_vspace[x] * valuable_space_count[i][x];
			/*printf("%d ", valuable_space_count[i][x]);*/
		}
		/*printf("\n");*/
	}

	/*printf("Color: %d\nDot: %d\n", values[0], values[1]);*/
    Py_DECREF(npy_board);
	return PyInt_FromLong(values[0] - values[1]);
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
        {
                "heuristic", heuristic, METH_VARARGS,
                "An improved heuristic.",
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
	for(int i = 0; i < 2; ++i)
		for(int j = 0; j < 4; ++j)
			for(int k = 0; k < 4; ++k)
				matching_cells[i][j][k] = 0;
	//matching_cells[0] is the matrix for the color
	matching_cells[0][0][0] = 1;
	matching_cells[0][1][1] = 1;
	matching_cells[0][2][2] = 1;
	matching_cells[0][3][3] = 1;
	matching_cells[0][0][1] = 1;
	matching_cells[0][1][0] = 1;
	matching_cells[0][2][3] = 1;
	matching_cells[0][3][2] = 1;
	//matching_cells[1] is the matrix for the dot
	matching_cells[1][0][0] = 1;
	matching_cells[1][1][1] = 1;
	matching_cells[1][2][2] = 1;
	matching_cells[1][3][3] = 1;
	matching_cells[1][0][2] = 1;
	matching_cells[1][2][0] = 1;
	matching_cells[1][1][3] = 1;
	matching_cells[1][3][1] = 1;
    return PyModule_Create(&hello_definition);
}