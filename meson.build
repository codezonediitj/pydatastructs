project('pydatastructs', 'cpp',
       version : '1.0.1-dev',
       default_options : ['cpp_std=c++17'])

if host_machine.system() == 'windows'
  add_project_arguments('/MD', language: 'cpp')
endif

python = import('python').find_installation(pure: false)

subdir('pydatastructs')
