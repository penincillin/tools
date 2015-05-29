#ifndef _RECTIFY_
#define _RECTIFY_
#include <vector>
#include <algorithm>
#include <string.h>
using namespace std;

typedef unsigned char byte;

class Rectify
{

    private:
        /*
           static void getMatrix(const int *src_pos, const int *size, double *mat){
           double x[4],y[4];
           for(int i=0; i<4; i++){ 
           x[i] = double(src_pos[2*i]);
           y[i] = double(src_pos[2*i+1]);
           }
           swap(x[2],x[3]); swap(y[2],y[3]);

           double len=double(size[0]), wid=double(size[1]);
        //cout << len << " " << wid << endl;
        mat[2] = double(x[0]); mat[5] = double(y[0]); mat[8]=1.0;
        double t[6];
        t[0] = x[1]-x[0]; t[1] = y[1]-y[0]; 
        t[2] = x[2]-x[0]; t[3] = y[2]-y[0];
        t[4] = x[3]-x[0]; t[5] = y[3]-y[0];
        double a3 = ((t[4]-t[0]-t[2])*(y[2]-y[3]) - (t[5]-t[1]-t[3])*(x[2]-x[3])) / ((y[2]-y[3])*(x[1]-x[3])-(x[2]-x[3])*(y[1]-y[3]));
        double b3 = ((t[4]-t[0]-t[2])*(y[1]-y[3]) - (t[5]-t[1]-t[3])*(x[1]-x[3])) / ((x[2]-x[3])*(y[1]-y[3])- (x[1]-x[3])*(y[2]-y[3]));
        mat[6] = a3/len; mat[7] = b3/wid;
        mat[0] = (t[0]+x[1]*a3)/len;
        mat[3] = (t[1]+y[1]*a3)/len;
        mat[1] = (t[2]+x[2]*b3)/wid;
        mat[4] = (t[3]+y[2]*b3)/wid;
        for(int i=0; i<9; i++)
        cout << mat[i] << ", ";
        cout << endl;
        }*/
        static bool SolveLinearSystem(int n, double *A, double *b, double *x){
            // P*A = L*U, b' = P*b
            int i, j, k;
            for(i=0; i<n-1; i++){
                // find the maximum |A(i:n, i)|
                j = i;
                for(k=i+1; k<n; k++) if(fabs(A[j*n+i])<fabs(A[k*n+i])) j = k;
                if(fabs(A[j*n+i])<1e-6) return false;

                // swap the two rows A(i,:) and A(j,:) and two elements b(i) and b(j)
                if(j>i){
                    for(k=0; k<n; k++){
                        double temp = A[i*n+k];
                        A[i*n+k] = A[j*n+k];
                        A[j*n+k] = temp;
                    }
                    double temp = b[i];
                    b[i] = b[j];
                    b[j] = temp;
                }
                // update A(i+1:n,i) /= A(i,i)
                for(k=i+1; k<n; k++) A[k*n+i] /= A[i*n+i];
                // update A(i+1:n,i+1:n) -= A(i+1:n,i)*A(i,i+1:n)
                for(j=i+1; j<n; j++)
                    for(k=i+1; k<n; k++) 
                        A[j*n+k] -= A[j*n+i]*A[i*n+k];
            }

            // Solve L*y = b'
            for(i=0; i<n; i++){
                x[i] = b[i];
                for(j=0; j<i; j++) x[i] -= x[j]*A[i*n+j];
            }
            // Solve U*x = y
            for(i=n-1; i>=0; i--){
                for(j=i+1; j<n; j++) x[i] -= x[j]*A[i*n+j];
                x[i] /= A[i*n+i];
            }
            return true;
        }




        static void getMatrix(const int *src_pos, const int *dst_pos, double *mat){
            double b[8];
            for(int i=0; i<8; i++) b[i] = double(src_pos[i]);
            double *A = new double[64];
            for(int i=0; i<8; i++){
                if(i%2==0){
                    A[i*8] = dst_pos[(i/2)*2];
                    A[i*8+1] = dst_pos[(i/2)*2+1];
                    A[i*8+2] = 1.0;
                    for(int j=3; j<6; j++) A[i*8+j] = 0.0;
                    A[i*8+6] = -src_pos[(i/2)*2]*dst_pos[(i/2)*2];
                    A[i*8+7] = -src_pos[(i/2)*2]*dst_pos[(i/2)*2+1];
                }
                else{
                    for(int j=0; j<3; j++) A[i*8+j] = 0.0;
                    A[i*8+3] = dst_pos[(i/2)*2];
                    A[i*8+4] = dst_pos[(i/2)*2+1];
                    A[i*8+5] = 1.0;
                    A[i*8+6] = -src_pos[(i/2)*2+1]*dst_pos[(i/2)*2];
                    A[i*8+7] = -src_pos[(i/2)*2+1]*dst_pos[(i/2)*2+1];
                }
            }
            SolveLinearSystem(8,A,b,mat);
            mat[8] = 1.0;
            delete [] A;
        }


    public: 
        static void imageRectify(const int *src_pos, const int* dst_pos, const int *src_size, int *dst_size, byte* src_data, byte* dst_data){
            double mat[9]; //item of transformation matrix
            int dst_wid=dst_size[0], dst_he=dst_size[1];
            int src_wid=src_size[0];
            getMatrix(src_pos, dst_pos, mat); //get transform matrix
            for(int i=0; i<dst_he; i++)
                for(int j=0; j<dst_wid; j++){
                    //compute A*x
                    double vec[3];
                    vec[0] = double(j); vec[1] = double(i); vec[2]=1.0;
                    double tmp[3];
                    tmp[0]=tmp[1]=tmp[2]=0.0;
                    for(int k=0; k<3; k++)
                        for(int l=0; l<3; l++)
                            tmp[k] += (vec[l])*mat[k*3+l];
                    //get corresponding x,y in source image
                    double x0 = tmp[0]/tmp[2];
                    double y0 = tmp[1]/tmp[2];
                    // two-dimensional linear interpolation
                    int x[4],y[4];
                    x[0] = floor(x0); y[0] = floor(y0);
                    x[1] = x[0]+1;    y[1] = y[0];
                    x[2] = x[0];      y[2] = y[0]+1;
                    x[3] = x[0]+1;    y[3] = y[0]+1;
                    double delta_x = 1.0-(x0-double(x[0]));
                    double delta_y = 1.0-(y0-double(y[0]));
                    for(int k=0; k<3; k++){
                        double tmp = (src_data[(y[0]*src_wid+x[0])*3+k]*delta_x + src_data[(y[1]*src_wid+x[1])*3+k]*(1-delta_x))*delta_y;
                        tmp += (src_data[(y[2]*src_wid+x[2])*3+k]*delta_x + src_data[(y[3]*src_wid+x[3])*3+k]*(1-delta_x))*(1-delta_y); 
                        dst_data[(i*dst_wid+j)*3+k] = (byte)tmp;
                    }
                    /* no-interpolation
                       int x = tmp[0]/tmp[2];
                       int y = tmp[1]/tmp[2];
                       dst_data[(i*dst_wid+j)*3+0] = src_data[(y*src_wid+x)*3+0];
                       dst_data[(i*dst_wid+j)*3+1] = src_data[(y*src_wid+x)*3+1];
                       dst_data[(i*dst_wid+j)*3+2] = src_data[(y*src_wid+x)*3+2];
                       */
                }
        }
};

#endif
