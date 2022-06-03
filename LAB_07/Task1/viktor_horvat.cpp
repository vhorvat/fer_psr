#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <boost/numeric/ublas/operation.hpp>
#include <boost/numeric/ublas/vector_expression.hpp>
#include <boost/numeric/ublas/vector_proxy.hpp>
#include <boost/numeric/ublas/matrix_proxy.hpp>
#include <boost/numeric/ublas/matrix_vector.hpp>

#include <boost/numeric/ublas/triangular.hpp>
#include <boost/numeric/ublas/lu.hpp>


int main() {
    using namespace boost::numeric::ublas;
    matrix<int> m1 (5,5);
    matrix<int> m2 (5,5);
    matrix<int> m3 (5,5);
    vector<int> v (5);
    vector<int> v1 (5);
    int i;

    for(i=0;i<m1.size1();i++){
        m1 (i,0) = 0;
        m1 (i,1) = 0;
        m1 (i,2) = 3;
        m1 (i,3) = 6;
        m1 (i,4) = 5;
    }
    std::cout<<m1<<std::endl;
    
    identity_matrix<int> m_temp (5);
    std::cout<<m_temp<<std::endl;

    m2=m_temp+m1;
    std::cout<<m2<<std::endl;

    v (0) = 1; 
    v (1) = 1;
    v (2) = 9;
    v (3) = 5;
    v (4) = 8;

    axpy_prod(m2,v,v1,true);
    std::cout << v1 <<std::endl;
    std::cout << inner_prod(v, trans(v)) << std::endl;
    std::cout << m1+m2 << std::endl;

/* KOD ZA INVERZ MATRICE NIJE MOJ ORIGINALAN RAD, IDEJA I DIJELOVI KODA PREUZETI SU SA STRANICA
    uBLAS REPOZITORIJA KOJI SLUŽBENO NIJE ODRŽAVAN OD STRANE ADMINISTRATORA 
    ALGORITAM I RJEŠENJE U NJEMU REFERENCIRANI SU NA:
    Reference: Numerical Recipies in C, 2nd ed., by Press, Teukolsky, Vetterling & Flannery. */

    matrix<double> m2_copy (5, 5);
    m2_copy=m2;

    permutation_matrix<double> pm(m2_copy.size1());
    
    matrix <double> inverse(5,5);
    for (int i = 0; i < inverse.size1 (); ++ i)
        for (int j = 0; j < inverse.size2 (); ++ j)
            if(i==j) inverse(i,j) = 1;
    
    int res = lu_factorize(m2_copy, pm);
    lu_substitute(m2_copy, pm, inverse);
    
    std::cout << inverse << std::endl;      


    return 0;

}