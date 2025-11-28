project('pydatastructs', 'cpp',
       version : '1.0.1-dev',
       default_options : ['cpp_std=c++17'])


python = import('python').find_installation(pure: false)

if host_machine.system() == 'darwin'
  arch = run_command('uname', '-m').stdout().strip()
  add_project_arguments('-arch', arch, language: 'cpp')
  add_project_link_arguments('-arch', arch, language: 'cpp')
endif

subdir('pydatastructs')
