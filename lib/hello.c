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

static PyObject* check_move(PyObject *dummy, PyObject *args)
{
	PyObject *arg_board=NULL;
	PyObject *npy_board=NULL;
	int type, recycling, x_move, y_move, x_rec, y_rec, card_to_rec;

	if (!PyArg_ParseTuple(args, "Opiiiiii", &arg_board, &recycling, &type, &x_move, &y_move, &x_rec, &y_rec, &card_to_rec))
		return NULL;

	npy_board = PyArray_FROM_OTF(arg_board, NPY_DOUBLE, NPY_IN_ARRAY);

	double const* board = PyArray_DATA(npy_board);

	npy_intp *shape_board = PyArray_SHAPE(npy_board);
	int width = shape_board[0];
	int height = shape_board[1];

	int shape_placement_pos[2] = {2, 2};
	int shape_no_empty[2] = {2, 2};
	int shape_recycling_pos[2] = {2, 2};
	int shape_empty[2] = {2, 2};
	int placement_pos[4];
	int no_empty[4];
	int recycling_pos[4];
	int empty[4];
	if(type == 1 || type == 3 || type == 5 || type == 7){
		placement_pos[0] = x_move;
		placement_pos[1] = y_move;
		placement_pos[2] = x_move+1;
		placement_pos[3] = y_move;
		no_empty[0] = x_move;
		no_empty[1] = y_move-1;
		no_empty[2] = x_move+1;
		no_empty[3] = y_move-1;
	}
	else{
		placement_pos[0] = x_move;
		placement_pos[1] = y_move;
		placement_pos[2] = x_move;
		placement_pos[3] = y_move+1;
		no_empty[0] = x_move;
		no_empty[1] = y_move-1;
		no_empty[2] = x_move;
		no_empty[3] = y_move-1;
	}
	if(recycling == 1){
		if(card_to_rec == 1 || card_to_rec == 3 || card_to_rec == 5 || card_to_rec == 7){
			empty[0] = x_rec;
			empty[1] = y_rec+1;
			empty[2] = x_rec+1;
			empty[3] = y_rec+1;
			recycling_pos[0] = x_rec;
			recycling_pos[1] = y_rec;
			recycling_pos[2] = x_rec+1;
			recycling_pos[3] = y_rec;
		}
		else{
			empty[0] = x_rec;
			empty[1] = y_rec+2;
			shape_empty[0] = 1;
			recycling_pos[0] = x_rec;
			recycling_pos[1] = y_rec;
			recycling_pos[2] = x_rec;
			recycling_pos[3] = y_rec+1;
		}
	}
	else{
		shape_recycling_pos[0] = 0;
		shape_empty[0] = 0;
	}
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
	return PyInt_FromLong(return_value);
}

inline void count_line(int const x_start,
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
	int prev_offset[2] = {-1, -1};
	int val_prev_poffset[2] = {-1, -1};
	int count[2];
#define safe_size_temp_line (12+8)
	int tmp_vspaces[2][safe_size_temp_line]; //12+8 is just to be sure we have enough space
	for(int i = 0; i < 2; ++i)
		for(int j = 0; j < safe_size_temp_line; ++j)
			tmp_vspaces[i][j] = 0;
	do{	
		//Compute the current x and y
		int x = x_start + offset*x_offset_mul;
		int y = y_start + offset*y_offset_mul;
		//Check if this position is on the board
		if(x < 0 || x >= shape_board[0] || y < 0 || y >= shape_board[1]){
			break;
		}
		//Get the real index and the current value
		int idx = x*shape_board[1] + y;
		int val = board[idx];
		/*First turn, we need to initialize count*/
		if(prev_val == -1){
			if(val != 0)
				count[0] = count[1] = 1;
			else{
				count[0] = count[1] = 0;
				prev_offset[0] = prev_offset[1] = offset;
			}
		}
		else{
			if(val == 0){
				if(prev_val > 0){ //The previous value wasn't empty, so we need to count a line of size count[i]
					for(int i = 0; i < 2; ++i){
						if(count[i] > 0){
							align[i][count[i]-1] += 1;
							tmp_vspaces[i][offset] += count[i];

							if(prev_offset[i] >= 0){
								int const po = prev_offset[i];
								int v = val_prev_poffset[i];
								if(v > 0 && matching_cells[i][prev_val-1][v-1]) //If the value before the previous space match our current line, combine the vspace
									tmp_vspaces[i][po] += count[i];
								else
									tmp_vspaces[i][po] = tmp_vspaces[i][po] < count[i] ? count[i] : tmp_vspaces[i][po];
							}
						}
					}
				}
				count[0] = count[1] = 0;
				prev_offset[0] = prev_offset[1] = offset;
				val_prev_poffset[0] = val_prev_poffset[1] = prev_val;
			}
			else if(prev_val == 0){
				count[0] = count[1] = 1;
			}
			else{
				/*For both color and dot, check if the previous value match the current value so the serie keep going.*/
				/*For instance, if prev_val and val indicate the same color or the same type of dot.*/
				for(int i = 0; i < 2; ++i){
					if (matching_cells[i][prev_val-1][val-1]){
						count[i] += 1;
					}
					else{
						if(prev_offset[i] >= 0){
							int const po = prev_offset[i];
							int v = val_prev_poffset[i];
							if(v != 0 && matching_cells[i][prev_val-1][v-1]) //If the value before the previous space match our current line, combine the vspace
								tmp_vspaces[i][po] += count[i];
							else
								tmp_vspaces[i][po] = tmp_vspaces[i][po] < count[i] ? count[i] : tmp_vspaces[i][po];
							prev_offset[i] = -1;
							val_prev_poffset[i] = -1;
						}
						count[i] = 1;
					}
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
				if(prev_offset[i] >= 0){
					int const po = prev_offset[i];
					int v = val_prev_poffset[i];
					if(v != 0 && matching_cells[i][prev_val-1][v-1]) //If the value before the previous space match our current line, combine the vspace
						tmp_vspaces[i][po] += count[i];
					else
						tmp_vspaces[i][po] = tmp_vspaces[i][po] < count[i] ? count[i] : tmp_vspaces[i][po];
				}
			}
		}
	}
	for(int i = 0; i < 2; ++i)
		for(int j = 0; j < offset; ++j){
			int const x = x_start + j*x_offset_mul;
			int const y = y_start + j*y_offset_mul;
			int const idx = x*shape_board[1] + y;
			int const current_vspace = valuable_space[i][idx];
			tmp_vspaces[i][j] = tmp_vspaces[i][j] <= 4 ? tmp_vspaces[i][j] : 4;
			valuable_space[i][idx] = current_vspace < tmp_vspaces[i][j] ? tmp_vspaces[i][j] : current_vspace;
		}
}
static PyObject* heuristic(PyObject *dummy, PyObject *args)
{
	PyObject *arg_board=NULL, *arg_weights=NULL;
	PyObject *npy_board=NULL, *npy_weights=NULL;
	int next_player;

	if (!PyArg_ParseTuple(args, "OOi", &arg_board, &arg_weights, &next_player))
		return NULL;

	npy_board = PyArray_FROM_OTF(arg_board, NPY_DOUBLE, NPY_IN_ARRAY);
	npy_weights = PyArray_FROM_OTF(arg_weights, NPY_DOUBLE, NPY_IN_ARRAY);

	double const* board = PyArray_DATA(npy_board);
	double const* weights = PyArray_DATA(npy_weights);

	npy_intp *shape_board = PyArray_SHAPE(npy_board);

	int valuable_space[2][96];
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
		if(col > 0 && col < 7){
			count_line(col, shape_board[1] - 1, -1, -1, board, shape_board, align, valuable_space);
			count_line(col, shape_board[1] - 1,  1, -1, board, shape_board, align, valuable_space);
		}
	}
	for(int row = 0; row < shape_board[1]; ++row){
		//Check row from (0, row)
		count_line(0, row, 1, 0, board, shape_board, align, valuable_space);
		if(row > 7){
			//Check diagonal from (0, row)
			count_line(0, row, 1, -1, board, shape_board, align, valuable_space);
			//Check cdiagonal from (shape_board[0]-1, row)
			count_line(shape_board[0]-1, row, -1, -1, board, shape_board, align, valuable_space);
		}
	}

	int valuable_space_count[2][4];
	int valuable_space_count_avail[2][4];
	for(int i = 0; i < 2; ++i)
		for(int j = 0; j < 4; ++j){
			valuable_space_count[i][j]=0;
			valuable_space_count_avail[i][j]=0;
		}

	for(int i = 0; i < 2; ++i)
		for(int y = shape_board[1]-1; y >= 0; --y)
			for(int x = 0; x < shape_board[0]; ++x){
				int val = valuable_space[i][x*shape_board[1]+y];
				if(val > 0){
					if(y - 2 < 0 || board[x*shape_board[1]+y-2] > 0)
						valuable_space_count_avail[i][val- 1] += 1;
					else
						valuable_space_count[i][val- 1] += 1;
				}
			}
	/*int weight_align[4] = {0, 3, 10, 1000000};*/
	/*int weight_vspace[4] = {0, 1, 8, 100000};*/
//2 vspace à 3 == victoire
	double* weight_align = weights;
	double* weight_vspace = weights+4;
	double* weight_vspace_avail = weights+8;

	
	/*for(int y = shape_board[1]-1; y >= 0; --y){*/
		/*for(int x = 0; x < shape_board[0]; ++x){*/
			/*printf("%d", valuable_space[0][x*shape_board[1]+y]);*/
		/*}*/
		/*printf("\t");*/
		/*for(int x = 0; x < shape_board[0]; ++x){*/
			/*printf("%d", valuable_space[1][x*shape_board[1]+y]);*/
		/*}*/
		/*printf("\n");*/
	/*}*/
	/*for(int i = 0; i < 2; ++i){*/
		/*printf("Weight:\t");*/
		/*for(int x = 0; x < 4; ++x)*/
			/*printf("%d ", align[i][x]);*/
		/*printf("\n");*/
		/*printf("Vspace:\t");*/
		/*for(int x = 0; x < 4; ++x)*/
			/*printf("%d ", valuable_space_count[i][x]);*/
		/*printf("\n");*/
		/*printf("Vspace av: ");*/
		/*for(int x = 0; x < 4; ++x)*/
			/*printf("%d ", valuable_space_count_avail[i][x]);*/
		/*printf("\n");*/
	/*}*/

	double values[2] = {0};
	for(int i = 0; i < 2; ++i){
		for(int x = 0; x < 4; ++x){
			values[i] += weight_align[x] * (double)align[i][x];
			values[i] += weight_vspace[x] * (double)valuable_space_count[i][x];
			if(i == next_player){
				int const xx = x < 3 ? x+1 : 3;
				values[i] += weight_align[xx] * (double)valuable_space_count_avail[i][x];
			}
			else{
				values[i] += weight_vspace_avail[x] * (double)valuable_space_count_avail[i][x];
			}

		}
	}

    Py_DECREF(npy_board);
	Py_DECREF(npy_weights);
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
                "check_move", check_move, METH_VARARGS,
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
